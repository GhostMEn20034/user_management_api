from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
    __abstract__ = True # Set to True to avoid a created table for this class
