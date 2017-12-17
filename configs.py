import os

app_dir = os.path.dirname(os.path.realpath(__file__))


class Configuration:
    APPLICATION_DIR = app_dir
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/app.db' % app_dir
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = b"6\xb3l k\x83\xbe<\xb2\xc4\xd3\xb4\xd1<\x87\x98\x06\xcb[\xf0\xcb~\xcb\xb7\x91\xcf\xd3\xd7h\xbb'EX\xfaq\xa5f\xc1\x93\x0eK!\x99\xcc}\xaa>\x88a\xe0\xd9,O\xa5\xc5J"
    BCRYPT_LOG_ROUNDS = 4
    # CERT_PATH = '../authentication/cert.pem'
    # KEY_PATH = '../authentication/key.pem'


class TestConfiguration:
    APPLICATION_DIR = app_dir
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/test_app.db' % app_dir
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = b"bebebe"
    BCRYPT_LOG_ROUNDS = 10
