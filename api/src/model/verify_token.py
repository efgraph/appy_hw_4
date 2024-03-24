from fastapi import Header, Depends
from jose import jwt

from core.config import settings
from db.redis_data_source import RedisDataSource
from model.exceptions import NotAuthenticated, NotFound
from model.injector import get_redis_data_source


class VerifyToken:
    def __init__(self, is_refresh=False):
        self.is_refresh = is_refresh

    def __call__(self, token: str = Header(...),
                 redis_data_source: RedisDataSource = Depends(get_redis_data_source)) -> str:
        try:
            payload = jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
            username: str = payload.get('sub')
            prefix = 'refresh_token' if self.is_refresh else 'access_token'
            if not redis_data_source.exists_token_in_cache(token, username, prefix):
                raise NotFound()
            return username
        except Exception:
            raise NotAuthenticated()
