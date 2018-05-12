import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db, app_config

app = app_config(app, os.environ.get('ENVIRONMENT'))

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
