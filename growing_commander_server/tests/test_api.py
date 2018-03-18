import json
import jsonpickle
import unittest
from datetime import datetime

from growing_commander_server import db
from growing_commander_server.models import User, Measurement
from growing_commander_server.tests.base import BaseTestCase


class TestMeasurementApiModel(BaseTestCase):
    def test_add_new_measurement_rest_api(self):
        jsonified_dataframe = '{"0":{"device_name":"Thermometer 1","measurement_type":"humidity","measurement_unit":"%","measurement_value":37.4500007629,"timestamp":"2018-01-03T18:21:53.008Z"},"1":{"device_name":"Thermometer 1","measurement_type":"temperature","measurement_unit":"*C","measurement_value":24.7000007629,"timestamp":"2018-01-03T18:21:53.008Z"}}'
        with self.client:
            auth_token = register_test_user_and_login(self)
            response = self.client.post(
                '/api/v1/measurement',
                data=json.dumps(dict(
                    auth_token=auth_token,
                    data=jsonified_dataframe
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['data']['added_items'], 2)
            self.assertEqual(Measurement.query.count(), 2)

    def test_add_new_measurement_rest_api_wrong_auth_token(self):
        jsonified_dataframe = '{"0":{"device_name":"Thermometer 1","measurement_type":"humidity","measurement_unit":"%","measurement_value":37.4500007629,"timestamp":"2018-01-03T18:21:53.008Z"},"1":{"device_name":"Thermometer 1","measurement_type":"temperature","measurement_unit":"*C","measurement_value":24.7000007629,"timestamp":"2018-01-03T18:21:53.008Z"}}'
        with self.client:
            response = self.client.post(
                '/api/v1/measurement',
                data=json.dumps(dict(
                    auth_token='wrong_token_941i41941-2-44weaaseasease',
                    data=jsonified_dataframe
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertIsInstance(data['message'], str)
            self.assertEqual(data['message'], "Invalid token. Please log in again.")
            self.assertEqual(Measurement.query.count(), 0)

    def test_post_no_data(self):
        with self.client:
            auth_token = register_test_user_and_login(self)
            response = self.client.post(
                '/api/v1/measurement',
                data=json.dumps(dict(
                    auth_token=auth_token
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], "No data provided to POST")
            self.assertEqual(Measurement.query.count(), 0)

    def test_get_measurements(self):

        # Add mock entries to database.
        m1 = Measurement(datetime.now(), "Device 1", 'Type 1', 15, '*C')
        m2 = Measurement(datetime.now(), "Device 1", 'Type 2', 256, 'MB')
        db.session.add(m1)
        db.session.add(m2)
        db.session.commit()

        with self.client:
            auth_token = register_test_user_and_login(self)
            response = self.client.get(
                '/api/v1/measurement',
                data=json.dumps(dict(
                    auth_token=auth_token
                )),
                content_type='application/json'
            )
            data = jsonpickle.decode(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(len(data['data']), 2)


def register_test_user_and_login(app):
    # Create user
    user = User("Name", "Password")
    db.session.add(user)
    db.session.commit()

    # registered user login
    response = app.client.post(
        'api/v1/auth/login',
        data=json.dumps(dict(
            name='Name',
            password='Password'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    return data['auth_token']

if __name__ == '__main__':
    unittest.main()
