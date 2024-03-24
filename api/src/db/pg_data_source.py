from db import User
from db.db import SessionLocal
from db.models import Image
from model.models import SignUpUser


class PostgresDataSource:
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_data(self):
        return self.db.get_data()

    def create_user(self, user: SignUpUser):
        user = User(**user.dict())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

    def create_image(self, username: str, image: str, prompt: str) -> Image:
        user = self.db.query(User).filter(User.username == username).first()
        image = Image(
            user_id=user.id,
            image=image,
            prompt=prompt
        )
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    def get_user_by_name(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
