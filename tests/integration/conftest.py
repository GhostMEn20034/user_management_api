import pytest
from flask import Flask
from sqlalchemy import create_engine, NullPool, text
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from src.core.app_factory import create_app
from src.models.base import BaseModel
from src.core.settings import get_settings


settings = get_settings()

test_engine = create_engine(settings.DB_CONNECTION_STRING, echo=False, poolclass=NullPool)


@pytest.fixture(scope='session')
def test_db_engine():
    BaseModel.metadata.drop_all(bind=test_engine)
    BaseModel.metadata.create_all(bind=test_engine)

    yield test_engine

    BaseModel.metadata.drop_all(bind=test_engine)

@pytest.fixture
def test_db_session(test_db_engine):
    """Creates a new transactional session for each test."""
    TestingSessionLocal = sessionmaker(expire_on_commit=False, autoflush=False, bind=test_db_engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close_all()

        # Truncate all tables and reset sequences
        meta = BaseModel.metadata
        with test_engine.connect() as conn:
            for table in reversed(meta.sorted_tables):
                conn.execute(text(f'TRUNCATE "{table.name}" CASCADE;'))
                conn.execute(text(f"ALTER SEQUENCE {table.name}_id_seq RESTART WITH 1;"))
            conn.commit()

@pytest.fixture()
def app() -> Flask:
    created_app = create_app("main")
    created_app.config.update({
        "TESTING": True,
    })

    # @created_app.teardown_appcontext
    # def remove_session(*args, **kwargs):
    #     app.session.remove()

    yield created_app


@pytest.fixture()
def client(app):
    return app.test_client()

