from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager, current_user

from growing_commander_server.configs import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

# https://github.com/cs50/problems/pull/24
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Imported here due to the circular dependencies.
# TODO: Figure out if there's a way to make it cleaner.
from growing_commander_server.views.auth import auth_blueprint
from growing_commander_server.views.measurement_api import measurement_api_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(measurement_api_blueprint)


@app.before_request
def _before_request():
    g.user = current_user
