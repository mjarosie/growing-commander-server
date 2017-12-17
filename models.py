import datetime
import jwt

from source import app, db, bcrypt
from source import login_manager


@login_manager.user_loader
def _user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, password, is_admin=False):
        self.name = name
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        )
        self.registered_on = datetime.datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return '<User #%i (%s)>'.format(self.id, self.friendly_name)

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)

    # Flask-Login interface..
    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def authenticate(name, password):
        user = User.query.filter(User.name == name).first()
        if user and user.check_password(password):
            return user
        return None


class ObservationGroup(db.Model):
    """ Model for storing observations consisting of multiple measurements (e.g. temperature, humidity, etc. """

    __tablename__ = "observation_group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    observation_start = db.Column(db.DateTime, nullable=False)
    observation_end = db.Column(db.DateTime, nullable=False)
    measurements = db.relationship('Measurement', backref='observation_group', lazy=False)

    def __init__(self, observation_start, observation_end):
        self.observation_start = observation_start
        self.observation_end = observation_end

    def __repr__(self):
        return '<ObservationGroup from {} to {}>'.format(self.observation_start, self.observation_end)


class Measurement(db.Model):
    """ Model for storing average values of measurements for a given observation group."""
    __tablename__ = "measurement"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)
    observation_group_id = db.Column(db.Integer, db.ForeignKey('observation_group.id'), nullable=False)

    def __init__(self, type, value, unit, observation_group_id):
        self.type = type
        self.value = value
        self.unit = unit
        self.observation_group_id = observation_group_id

    def __repr__(self):
        return '<Measurement {}: {}{}>'.format(self.type, self.value, self.unit)
