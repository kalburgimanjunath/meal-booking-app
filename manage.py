import os
from app import create_application
from flask_script import Manager, Shell
from app.models import User, data, MealOption

app = create_application(os.getenv('MEAL_APP_CONFIG') or 'default')

manager = Manager(app)


def make_shell_context():
    return dict(app=app, User=User, data=data)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def test():
    "Function to run unit tests"
    import unittest
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    return not result.wasSuccessful()


if __name__ == '__main__':
    manager.run()
