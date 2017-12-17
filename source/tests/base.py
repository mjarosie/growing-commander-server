from flask_testing import TestCase
from source import app, db

from source.configs import TestConfiguration


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object(TestConfiguration)
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


db.drop_all()
