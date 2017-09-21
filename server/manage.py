import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app import models

app = create_app("testing")
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Runs the unit tests without tests coverage."""
    tests = unittest.TestLoader().discover("./tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if(result.wasSuccessful()):
        return 0
    return 1

if(__name__ == "__main__"):
    manager.run()
