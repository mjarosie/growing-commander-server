from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager, current_user

from source.configs import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

manager.add_command('db', MigrateCommand)

@app.before_request
def _before_request():
    g.user = current_user
