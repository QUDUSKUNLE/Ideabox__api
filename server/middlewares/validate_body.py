from functools import wraps
from flask import request, jsonify


def validate_request(f):
    @wraps(f)
    def validate(*args, **kwargs):
        for key in list(request.get_json().keys()):
            if key not in ['name', 'password', 'email']:
                return jsonify(dict(
                    data=dict(
                        message='Invalid request'
                    ),
                    status='fail'
                )), 405

            elif (request.get_json()[key]).strip() == '':
                return jsonify(dict(
                    data=dict(
                        message='{} field can not be empty'.format(key)
                    ),
                    status='fail'
                )), 405

        if len(request.get_json()['name']) < 3:
            return jsonify(dict(
                data=dict(
                    message='User name must be greater than two characters'
                ),
                status='fail'
            )), 405
        elif len(request.get_json()['password']) < 6:
            return jsonify(dict(
                data=dict(
                    message='password is short and should be more than \
                    six characters'
                ),
                status='fail'
            )), 405

        elif (
            (request.get_json()['email']).find('@') == -1 or (
                request.get_json()['email']).find('.') == -1):
            return jsonify(dict(
                data=dict(
                    message='Invalid email address'
                ),
                status='fail'
            )), 405
        return f(*args, **kwargs)
    return validate
