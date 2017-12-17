import unittest
from datetime import datetime

from source import db
from source.models import User, Measurement, ObservationGroup
from source.tests.base import BaseTestCase
from sqlalchemy.exc import IntegrityError

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
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == 1)


class TestMeasurementModel(BaseTestCase):
    def test_adding_new_measurement_no_observation_group(self):
        measurement = Measurement("temperature", 25.0, "C", 10)
        db.session.add(measurement)
        db.session.commit()
        print('xDDD')
        # db.session.commit()
        #
        # self.assertRaises(IntegrityError, )

    def test_adding_new_measurement_existing_observation_group(self):
        obs_group = ObservationGroup(datetime(2017, 5, 5), datetime(2017, 5, 6))
        db.session.add(obs_group)
        db.session.commit()

        measurement = Measurement("temperature", 25.0, "C", obs_group.id)
        db.session.add(measurement)
        db.session.commit()
        self.assertEqual(measurement.query.count(), 1)


if __name__ == '__main__':
    unittest.main()
