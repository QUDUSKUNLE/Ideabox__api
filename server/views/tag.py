from flask import jsonify, request
from flask_restful import Resource

from ..auth import validate_token
from ..middlewares import PushID
from ..model import Tag, db


class TagResources(Resource):
    @validate_token
    def post(self):
        tag = request.get_json()

        for i in ['status']:
            if i not in tag.keys():
                response = jsonify(dict(
                    data=dict(
                        message='{} is required'.format(i)
                    ),
                    status='fail'
                ))
                response.status_code = 401
                return response

            for i, v in tag.items():
                if tag[i].strip() == '':
                    response = jsonify(dict(
                        data=dict(
                            message='{} can not be empty'.format(i)
                        ),
                        status='fail'
                    ))

                    response.status_code = 401
                    return response

                elif v not in ['Public', 'Private']:
                    response = jsonify(dict(
                        data=dict(
                            message='Status can either be public or private'
                        ),
                        status='fail'
                    ))
                    response.status_code = 401
                    return response

        # Check if tag already created
        check_tag = Tag.query.filter_by(idea_tag=tag['status']).first()
        if check_tag:
            response = jsonify(dict(
                data=dict(
                    message='Tag already exists'
                ),
                status='fail'
            ))
            response.status_code = 409
            return response

        new_tag = Tag(
            id=PushID().next_id(),
            idea_tag=tag['status']
        )
        db.session.add(new_tag)
        db.session.commit()

        response = jsonify(dict(
            data=dict(
                message='Tag status created successfully'
            ),
            status='success'
        ))
        response.status_code = 201
        return response
