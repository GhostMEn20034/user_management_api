from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.settings import get_settings

settings = get_settings()

engine = create_engine(settings.DB_CONNECTION_STRING)
SessionLocal = sessionmaker(expire_on_commit=False, autoflush=False, bind=engine)
