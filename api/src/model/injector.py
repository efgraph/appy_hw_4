from functools import lru_cache

from fastapi import Depends

import redis

from core.config import settings
from db.db import SessionLocal
from db.pg_data_source import PostgresDataSource
from db.redis_data_source import RedisDataSource
from service.auth_service import AuthService, AuthServiceImpl
from service.img_service import ImageService, ImageServiceImpl


@lru_cache()
def get_redis() -> redis.Redis:
    return redis.Redis(host=settings.redis.host, port=settings.redis.port, db=0,
                       decode_responses=True)


@lru_cache()
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


@lru_cache()
def get_redis_data_source(redis_client=Depends(get_redis)) -> RedisDataSource:
    return RedisDataSource(redis_client)


@lru_cache()
def get_pg_data_source(pg_client=Depends(get_db)) -> PostgresDataSource:
    return PostgresDataSource(pg_client)


def get_auth_service(redis_data_source: RedisDataSource = Depends(get_redis_data_source),
                     pg_datasource: PostgresDataSource = Depends(get_pg_data_source)) -> AuthService:
    return AuthServiceImpl(redis_data_source, pg_datasource)


def get_img_service(redis_data_source: RedisDataSource = Depends(get_redis_data_source),
                    pg_datasource: PostgresDataSource = Depends(get_pg_data_source)) -> ImageService:
    return ImageServiceImpl(redis_data_source, pg_datasource)
