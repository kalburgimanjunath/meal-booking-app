import os


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'Andela-is-awesome'
    ORDER_EXPIRES_IN = 5

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    TESTING = True


config = {
    'testing': TestingConfig,

    'default': Config
}
