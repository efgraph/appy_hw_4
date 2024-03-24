import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


def build_dsn(
        protocol: str,
        user: str,
        password: str,
        host: str,
        port: int,
        name: str,
) -> str:
    dsn = f'{protocol}://{user}:{password}@{host}:{port}/{name}'
    print(dsn)
    return dsn


class DatabaseSettings(BaseSettings):
    protocol: str = 'postgresql+psycopg'
    user: str = os.environ['POSTGRES_USER']
    password: str = os.environ['POSTGRES_PASSWORD']
    host: str = os.environ['POSTGRES_HOST']
    port: int = os.environ['POSTGRES_PORT']
    name: str = os.environ['POSTGRES_DB']
    db_url: str = os.environ['DB_URL']

    @property
    def dsn(self) -> str:
        return build_dsn(
            protocol=self.protocol,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            name=self.name,
        )


class RedisSettings(BaseSettings):
    host: str = os.environ['REDIS_HOST']
    port: int = os.environ['REDIS_PORT']


class JWTSettings(BaseSettings):
    secret_key: str = os.environ['JWT_SECRET_KEY']
    algorithm: str = os.environ['JWT_ALGORITHM']
    refresh_token_expire_days: int = 7
    access_token_expire_minites: int = 15


class WSGISettings(BaseSettings):
    host: str = 'localhost'
    port: int = 5000
    workers: int = 4


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    jwt: JWTSettings = JWTSettings()
    wsgi: WSGISettings = WSGISettings()


settings = Settings()
