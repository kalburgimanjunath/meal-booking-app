import os
from app import create_application, db
from flask_script import Manager, Shell
from app.models import User, Meal
from flask_migrate import Migrate, MigrateCommand

app = create_application(os.getenv('MEAL_APP_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    "Function to run unit tests"
    import unittest
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    return not result.wasSuccessful()


@manager.command
def initialize():
    """
     Initialize application by inserting roles
    """
    from flask_migrate import upgrade
    from app.models import Role

    upgrade()
    Role.insert_roles()


if __name__ == '__main__':
    manager.run()
