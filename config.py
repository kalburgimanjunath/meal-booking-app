"""
Module contains the configurations for the application
"""
import os


class Config:
    """
    Config class
    """
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'Andela-is-awesome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORDER_EXPIRES_IN = 5
    DATA_FOLDER = 'app/static'
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
    # amazon s3 keys
    S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
    S3_KEY = os.environ.get('S3_ACCESS_KEY')
    S3_SECRET = os.environ.get('S3_SECRET_ACCESS_KEY')
    S3_LOCATION = 'https://{}.s3.amazonaws.com/'.format(S3_BUCKET)

    @staticmethod
    def init_app(app):
        """
        initialises app with the config file
        """
        pass


class DevConfig(Config):
    """
      Configurations for development
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://andela1:AnDELa@localhost/bookamealdb')


class HerokuConfig(Config):
    """
    Configuration for heroku app
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG = False


class TestingConfig(Config):
    """
     Configurations for testing
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL',
        'postgresql://andela1:AnDELa@localhost/test_bookamealdb')


config = {
    'testing': TestingConfig,
    'default': DevConfig
}
