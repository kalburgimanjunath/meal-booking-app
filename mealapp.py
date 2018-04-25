import os

from app import create_application
from flask_script import Manager, Shell
from app.models import User, data

app = create_application(os.getenv('MEAL_APP_CONFIG') or 'default')

# create a flask script manager
manager = Manager(app)


def make_shell_context():
    return dict(app=app, User=User, data=data)


manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
