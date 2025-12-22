from flask import Flask
from .clients import get_qdb_client, get_genai_client

def create_app(test_config = None):
    #Flask application
    app = Flask(__name__)
    get_qdb_client()
    get_genai_client()

    if test_config is None:
        app.config.from_pyfile('../config.py')

    else:
        app.config.from_mapping(test_config)

    from .routes import bp
    app.register_blueprint(bp)

    return app
