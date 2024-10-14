from flask import Flask, session
from flask_smorest import Api
import uuid
import logging
from flask_cors import CORS

from .config.config import environment, port, db_name, db_user, db_pass, app_secret_key, external_host
from .api.chat_route import blp as MessageBlueprint
from .db import db

logging.basicConfig(level=logging.INFO)


def create_app():
    app = Flask(__name__)
    app.secret_key = app_secret_key  # Required for session management
    app.config["API_TITLE"] = "Message API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://unpkg.com/swagger-ui-dist/"
    app.config["MAX_CONTENT_LENGTH"] = 6 * 1024  # 6 kB
    if environment == "development":
        app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@db:5432/{db_name}"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@{external_host}:5432/{db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SESSION_PERMANENT"] = False

    # Configure CORS
    CORS(app)
    db.init_app(app)
    api = Api(app)
    api.register_blueprint(MessageBlueprint)

    @app.before_request
    def initialize_session_id():
        # Set the session_id from the environment variable
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())

    with app.app_context():
        db.create_all()

    return app


app = create_app()


def main():
    if environment == "production":
        app.run(host="0.0.0.0", port=port)
    elif environment == "development":
        app.run(host="0.0.0.0", debug=True, port=port)
    else:
        raise ValueError("Invalid environment")


if __name__ == "__main__":
    main()
