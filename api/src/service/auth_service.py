from abc import ABC, abstractmethod
from datetime import timedelta, datetime

from jose import jwt

from common.utils import hash_password, check_password
from core.config import settings
from db import User
from db.pg_data_source import PostgresDataSource
from db.redis_data_source import RedisDataSource
from model.exceptions import AlreadyRegistered, NotAuthenticated
from model.models import SignUpUser, AuthUser, Tokens


class AuthService(ABC):
    @abstractmethod
    async def signup_user(self, auth_data: SignUpUser) -> dict[str, any]:
        pass

    @abstractmethod
    async def authenticate_user(self, auth_data: AuthUser) -> Tokens:
        pass

    @abstractmethod
    async def update_tokens(self, username) -> Tokens:
        pass

    @abstractmethod
    async def delete_tokens(self, username):
        pass


class AuthServiceImpl(AuthService):
    def __init__(self, redis_data_source: RedisDataSource, pg_data_source: PostgresDataSource):
        self.redis_data_source = redis_data_source
        self.pg_data_source = pg_data_source

    async def signup_user(self, auth_data: SignUpUser) -> dict[str, any]:
        user = await self._get_user_by_name(auth_data.username)
        if user:
            raise AlreadyRegistered()
        auth_data.password = hash_password(auth_data.password)
        self.pg_data_source.create_user(auth_data)
        return auth_data.dict(exclude={'password'})

    async def authenticate_user(self, auth_data: AuthUser) -> Tokens:
        user = await self._get_user_by_name(auth_data.username)
        if not (user and check_password(auth_data.password, user.password)):
            raise NotAuthenticated()
        tokens = await self.update_tokens(user.username)
        return tokens

    async def update_tokens(self, username):
        access_token = await self._create_access_token(username)
        refresh_token = await self._create_refresh_token(username)
        return Tokens(access_token=access_token, refresh_token=refresh_token)

    async def _create_access_token(self, username: str):
        expire = datetime.utcnow() + timedelta(days=settings.jwt.access_token_expire_minites)
        to_encode = {"sub": username, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
        self.redis_data_source.put_token_to_cache(username, encoded_jwt, 'access_token',
                                                  15 * settings.jwt.access_token_expire_minites)
        return encoded_jwt

    async def _create_refresh_token(self, username: str):
        expire = datetime.utcnow() + timedelta(days=settings.jwt.refresh_token_expire_days)
        to_encode = {"sub": username, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
        self.redis_data_source.put_token_to_cache(username, encoded_jwt, 'refresh_token',
                                                  60 * 60 * 24 * settings.jwt.refresh_token_expire_days)
        return encoded_jwt

    async def delete_tokens(self, username):
        for prefix in ['access_token', 'refresh_token']:
            self.redis_data_source.delete_token_from_cache(username, prefix)

    async def _get_user_by_name(self, username: str) -> User | None:
        user = self.pg_data_source.get_user_by_name(username)
        return user if user else None
