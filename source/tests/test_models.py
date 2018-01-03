import unittest
from datetime import datetime

from source import db
from source.models import User, Measurement
from tests.base import BaseTestCase


class TestUserModel(BaseTestCase):
    def test_login_correct_password(self):
        user = User(
            name='bombelek',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        login_result = user.authenticate('bombelek', 'test')
        self.assertEqual(login_result, user)

    def test_login_incorrect_password(self):
        user = User(
            name='bombelek',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        login_result = user.authenticate('bombelek', 'bad_password')
        self.assertIsNone(login_result)

    def test_encode_auth_token(self):
        user = User(
            name='bombelek',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            name='bombelek',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)

        decoded_token_value = User.decode_auth_token(auth_token)
        self.assertTrue(decoded_token_value == user.id)


class TestMeasurementModel(BaseTestCase):
    def test_adding_new_measurement(self):
        measurement = Measurement(datetime.now(), "Device 1", "temperature", 25.0, "C")
        db.session.add(measurement)
        db.session.commit()

        self.assertEqual(Measurement.query.count(), 1)

    def test_adding_multiple_new_measurements(self):
        measurement_1 = Measurement(datetime.now(), "Device 1", "temperature", 25.0, "C")
        measurement_2 = Measurement(datetime.now(), "Device 1", "humidity", 30.0, "%")

        measurement_3 = Measurement(datetime.now(), "Device 2", "temperature", 27.0, "C")
        measurement_4 = Measurement(datetime.now(), "Device 2", "humidity", 33.0, "%")
        measurements = [measurement_1, measurement_2, measurement_3, measurement_4]

        for measurement in measurements:
            db.session.add(measurement)

        db.session.commit()
        self.assertEqual(Measurement.query.count(), 4)


if __name__ == '__main__':
    unittest.main()
