from flask import Flask
from greenlet import getcurrent
from sqlalchemy.orm import scoped_session

from src.extensions import api

from src.resources.healthcheck import healthcheck_ns
from src.resources.user import user_ns
from .database import SessionLocal


def create_app(flask_import_name: str) -> Flask:
    app = Flask(flask_import_name)
    app.session = scoped_session(SessionLocal, scopefunc=getcurrent)

    api.init_app(app)

    api.add_namespace(healthcheck_ns)
    api.add_namespace(user_ns, path='/api/v1')

    return app
