from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config


db = SQLAlchemy()


def create_application(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    return app
