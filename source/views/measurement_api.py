import pandas as pd
import json
from datetime import datetime

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

measurement_api_blueprint = Blueprint('measurement_api', __name__)

from source import db
from source.models import User, Measurement


class MeasurementAPI(MethodView):
    """
    Measurement API Resource
    """

    def post(self):
        auth_token = request.get_json().get('auth_token')
        try:
            auth_response = User.decode_auth_token(auth_token)
        except ValueError as e:
            response_object = {
                'status': 'fail',
                'message': str(e)
            }
            return make_response(jsonify(response_object)), 401

        # get the post data
        post_data_json = request.get_json().get('data')
        post_data = json.loads(post_data_json)

        # Create a dataframe from json data.
        df = pd.DataFrame.from_dict(post_data, orient='index')
        df.timestamp = pd.to_datetime(df.timestamp)

        # Add each row to database.

        for i, row in df.iterrows():
            m = Measurement(row['timestamp'], row['device_name'], row['measurement_type'], row['measurement_value'], row['measurement_unit'])
            db.session.add(m)
        db.session.commit()

        response_object = {
            'status': 'success',
            'data': {
                'added_items': len(df)
            }
        }
        return make_response(jsonify(response_object)), 200


measurement_view = MeasurementAPI.as_view('login_api')

measurement_api_blueprint.add_url_rule(
    '/measurement',
    view_func=measurement_view,
    methods=['POST']
)
