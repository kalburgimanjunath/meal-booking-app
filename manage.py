import os
from app import create_application
from flask_script import Manager, Shell
from app.models import User, data, MealOption

app = create_application(os.getenv('MEAL_APP_CONFIG') or 'default')

manager = Manager(app)

# create a test user
test_user = User(name='test', email='test@test.com')
test_user.password = 'test'
test_user.save()

# create a test admin user
admin_user = User('admin', email='admin@admin.com')
admin_user.password = 'admin'
admin_user.is_admin = True
admin_user.save()

# create a test meal
meal = MealOption('lorem meal', 10000)
meal.save()

meal = MealOption('Beef with rice', 1500)
meal.save()


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
