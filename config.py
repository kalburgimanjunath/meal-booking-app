import os


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'Andela-is-awesome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORDER_EXPIRES_IN = 5

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    """
      Configurations for development
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL',
        'postgresql://andela1:AnDELa@localhost/bookamealdb')


class TestingConfig(Config):
    """
     Configurations for testing
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL',
        'postgresql://andela1:AnDELa@localhost/test_bookamealdb')


config = {
    'testing': TestingConfig,

    'default': DevConfig
}
