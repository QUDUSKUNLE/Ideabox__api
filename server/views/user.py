import uuid

from flask import g, jsonify, request
from flask_restful import Resource
from werkzeug.security import check_password_hash

from ..auth import validate_token
from ..middlewares import (
    hashed_password,
    generate_token,
    PushID,
    validate_request
)
from ..model import User, db
from ..service import MailService


class NewUserResources(Resource):

    @validate_request
    def post(self):
        user = User.query.filter_by(
            email=request.get_json()['email'].strip()
        ).first()
        if user:
            response = jsonify(dict(
                data=dict(
                    message='Email already exist'
                ),
                status='fail'
            ))
            response.status_code = 409
            return response

        hashPass = hashed_password(request.get_json()['password'])
        publicId = PushID().next_id()
        user_request = dict(
            name=request.get_json()['name'].strip(),
            id=publicId
        )
        new_user = User(
            name=request.get_json()['name'].strip(),
            email=request.get_json()['email'].strip(),
            password=hashPass,
            id=publicId
        )
        db.session.add(new_user)
        db.session.commit()

        response = jsonify(dict(
            data=dict(
                message=user_request,
                token='Bearer {}'.format(generate_token(dict(id=publicId)))
            ),
            status='success'
        ))
        response.status_code = 201
        return response


class UserResources(Resource):

    def post(self):
        user = request.get_json()
        query_user_data = User.query.filter_by(email=user['email']).first()

        if not query_user_data:
            response = jsonify(dict(
                data=dict(
                    message='User not found'
                ),
                status='fail'
            ))
            response.status_code = 404
            return response

        # Check user password
        if not check_password_hash(query_user_data.password, user['password']):
            response = jsonify(dict(
                data=dict(
                    message='Incorrect username or password'
                ),
                status='fail'
            ))
            response.status_code = 401
            return response

        response = jsonify(dict(
            data=dict(
                message='logged in successful',
                token='Bearer {}'.format(
                    generate_token(dict(id=query_user_data.id))
                )
            ),
            status='success'
        ))
        response.status_code = 200
        return response


class ResetPasswordResources(Resource):

    @validate_token
    def post(self):
        user = User.query.filter_by(id=g.current_user['id']).first()
        if not user:
            response = jsonify(dict(
                data=dict(
                    message='User not found'
                ),
                status='fail'
            ))
            response.status_code = 401
            return response
        password_link = uuid.uuid4().hex
        user.reset_password_link = password_link
        db.session.commit()

        # email = dict(
        #     config=app,
        #     recipient=[user.email],
        #     link=password_link
        # )
        # MailService().reset_password_mail(email)
        response = jsonify(dict(
            data=dict(
                message='Email reset link sent successfully'
            ),
            status='success'
        ))
        response.status_code = 201
        return response
