from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from growing_commander_server.models import User

auth_blueprint = Blueprint('auth', __name__)


class AuthorizationAPI(MethodView):
    """
    Authorization API Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        if post_data is None:
            response_object = {
                'status': 'fail',
                'message': 'No data provided'
            }
            return make_response(jsonify(response_object)), 400
        if 'name' not in post_data or 'password' not in post_data:
            response_object = {
                'status': 'fail',
                'message': 'Incorrect login or password'
            }
            return make_response(jsonify(response_object)), 401
        user = User.authenticate(post_data['name'], post_data['password'])
        if user is None:
            response_object = {
                'status': 'fail',
                'message': 'Incorrect login or password'
            }
            return make_response(jsonify(response_object)), 401
        try:
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
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(response_object)), 500


authorization_view = AuthorizationAPI.as_view('login_api')

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=authorization_view
)
