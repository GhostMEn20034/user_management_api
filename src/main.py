from src.core.app_factory import create_app


app = create_app(__name__)

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()
