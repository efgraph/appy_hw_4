from sqlalchemy.orm import declarative_base
from core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine(settings.db.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
