import unittest
import json
from source import db
from source.models import User
from source.tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # Create user
            user = User("Name", "Password")
            db.session.add(user)
            db.session.commit()

            # registered user login
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    name='Name',
                    password='Password'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()