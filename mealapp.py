import os

from app import create_application

app = create_application(os.getenv('MEAL_APP_CONFIG') or 'default')
