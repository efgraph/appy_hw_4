from redis import Redis


class RedisDataSource:

    def __init__(self, redis: Redis):
        self.redis = redis

    def put_token_to_cache(self, username, token, prefix, expire):
        self.redis.set(f"{prefix}:{username}", token, ex=expire)

    def exists_token_in_cache(self, token, username, prefix) -> bool:
        stored_token = self.redis.get(f'{prefix}:{username}')
        return token == stored_token

    def delete_token_from_cache(self, username, prefix):
        self.redis.delete(f'{prefix}:{username}')

    def put_prompt_to_cache(self, prompt, image_id, expire):
        self.redis.set(f'{prompt}', image_id, ex=expire)

    def get_prompt_from_cache(self, prompt):
        return self.redis.get(f'{prompt}')
