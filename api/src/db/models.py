import datetime

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey

from db.db import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class Image(Base):
    __tablename__ = "image"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    image = Column(String, unique=True)
    prompt = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
