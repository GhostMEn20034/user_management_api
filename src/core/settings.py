import os
from functools import lru_cache


class Settings:
    DB_CONNECTION_STRING: str

    def __init__(self, db_connection_string: str):
        self.DB_CONNECTION_STRING = db_connection_string


@lru_cache
def get_settings() -> Settings:
    db_connection_string = os.getenv('DB_CONNECTION_STRING')

    return Settings(db_connection_string)