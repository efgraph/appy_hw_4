import os
import uuid
from abc import ABC, abstractmethod
import random
from db import models
from PIL import Image

from db.pg_data_source import PostgresDataSource
from db.redis_data_source import RedisDataSource


class ImageService(ABC):
    @abstractmethod
    async def get_image_by_prompt(self, username: str, gen_path: str, prompt: str) -> str:
        pass


class ImageServiceImpl(ImageService):
    def __init__(self, redis_data_source: RedisDataSource, pg_data_source: PostgresDataSource):
        self.redis_data_source = redis_data_source
        self.pg_data_source = pg_data_source

    async def get_image_by_prompt(self, username: str, gen_path: str, prompt: str) -> str:
        image_id = self.redis_data_source.get_prompt_from_cache(prompt)
        if not image_id:
            img = await self._create_image(username, gen_path, prompt)
            self.redis_data_source.put_prompt_to_cache(prompt, img.image, 3600 * 24)
            image_id = img.image
        return image_id

    async def _create_image(self, username: str, gen_path: str, prompt: str) -> models.Image:
        img = Image.new('RGB', (512, 512), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        image_id = f'{str(uuid.uuid4())}.png'
        img.save(os.path.join(gen_path, image_id), 'png')
        image = self.pg_data_source.create_image(username, image_id, prompt)
        return image
