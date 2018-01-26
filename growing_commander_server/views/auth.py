from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

auth_blueprint = Blueprint('auth', __name__)

from models import User


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                name=post_data.get('name')
            ).first()
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500


login_view = LoginAPI.as_view('login_api')

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
