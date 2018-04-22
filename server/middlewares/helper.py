import datetime
import jwt
import os

from werkzeug.security import generate_password_hash


def generate_token(req):
    return (jwt.encode({
        'id': req['id'].strip(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1440)},
        os.environ.get('SECRET_KEY'),
        algorithm='HS256')).decode("UTF-8")


def hashed_password(password):
    return generate_password_hash(password, method='sha256', salt_length=25)
