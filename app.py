import os

from flask import Flask
from flask_smorest import Api

from db import db
import models

from resources.domain import Bip as Domain
from resources.page import Bip as Page


def create_app(db_url=None, testing=True):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = testing
    if app.config["TESTING"]:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL", "sqlite:///test_datas.sqlite")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///datas.sqlite")
    db.init_app(app)

    @app.before_request
    def create_tables():
        db.create_all()

    api = Api(app)
    api.register_blueprint(Domain)
    api.register_blueprint(Page)
    return app


if __name__ == "__main__":
    app = create_app(testing=False)
    app.run(host='0.0.0.0', port=5050, debug=True)
