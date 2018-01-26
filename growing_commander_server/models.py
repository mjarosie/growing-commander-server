import datetime
import jwt

from growing_commander_server import app, db, bcrypt, login_manager


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
            raise ValueError('Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid token. Please log in again.')

    @staticmethod
    def authenticate(name, password):
        user = User.query.filter(User.name == name).first()
        if user and user.check_password(password):
            return user
        return None


class Measurement(db.Model):
    """ Model for storing average values of measurements for a given observation group."""
    __tablename__ = "measurement"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    device_name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)

    def __init__(self, timestamp, device_name, type, value, unit):
        self.timestamp = timestamp
        self.device_name = device_name
        self.type = type
        self.value = value
        self.unit = unit

    def __repr__(self):
        return '<Measurement of {} taken at {} from {}: {}{}>'.format(self.type, self.timestamp, self.device_name, self.value, self.unit)
