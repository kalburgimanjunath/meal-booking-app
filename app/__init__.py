from flask import Flask
from config import config


def create_application(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .api_1_0 import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    return app
