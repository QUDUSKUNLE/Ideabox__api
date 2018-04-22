import os
import jwt

from functools import wraps
from flask import g, request, jsonify

NO_BEARER_MSG = (
    "Invalid Token. The token should begin with the word 'Bearer '."
)
NO_TOKEN_MSG = (
    "Bad request. Header does not contain an authorization token. Log into"
)


def validate_token(f):
    @wraps(f)
    def validate(*args, **kwargs):
        authorization_token = request.headers.get('Authorization')
        if not authorization_token:
            response = jsonify(dict(
                status='fail',
                data=dict(
                    message=NO_TOKEN_MSG
                )
            ))
            response.status_code = 401
            return response

        # validates the word bearer is in the token
        if 'bearer ' not in authorization_token.lower():
            response = jsonify(dict(
                status='fail',
                data=dict(
                    message=NO_BEARER_MSG
                )
            ))

            response.status_code = 400
            return response

        try:
            authorization_token = authorization_token.split(' ')[1]
            payload = jwt.decode(
                authorization_token,
                os.environ.get('SECRET_KEY'),
                algorithms=['HS256'],
                options={
                    'verify_signature': True,
                    'verify_exp': True
                }
            )

        except jwt.exceptions.DecodeError:
            response = jsonify(dict(
                data=dict(
                    message='Invalid Token'
                ),
                status='fail'
            ))
            response.status_code = 401
            return response

        except jwt.InvalidAlgorithmError:
            response = jsonify(dict(
                data=dict(
                    message='Invalid Algorithm token'
                ),
                status='fail'
            ))

            response.status_code = 405
            return response

        except jwt.ExpiredSignatureError:
            response = jsonify(dict(
                data=dict(
                    message='Token is expired'
                ),
                status='fail'
            ))

            response.status_code = 401
            return response

        g.current_user = payload
        return f(*args, **kwargs)

    return validate
