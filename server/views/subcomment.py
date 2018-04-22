from flask import g, jsonify, request
from flask_restful import Resource

from ..auth import validate_token
from ..middlewares import PushID
from ..model import User, Comment, SubComment, db


class SubCommentResource(Resource):

    @validate_token
    def post(self):

        subcomment_request = request.get_json()
        subcomment_poster = User.query.filter_by(
            id=g.current_user['id']
        ).first()

        if not subcomment_poster:
            response = jsonify(dict(
                data=dict(
                    message='User not Found'
                ),
                status='fail'
            ))
            response.status_code = 404
            return response

        for i in ['subcomment', 'comment_id']:
            if i not in subcomment_request.keys():
                response = jsonify(dict(
                    data=dict(
                        message='{} is required'.format(i)
                    ),
                    status='fail'
                ))
                response.status_code = 400
                return response

            if subcomment_request[i].strip() == '':
                response = jsonify(dict(
                    data=dict(
                        message='{} can not be empty'.format(i)
                    ),
                    status='fail'
                ))
                response.status_code = 400
                return response

        subcomment_comment = Comment.query.filter_by(
            id=subcomment_request['comment_id'].strip()
        ).first()

        if not subcomment_comment:
            response = jsonify(dict(
                data=dict(
                    message='Comment not Found'
                ),
                status='fail'
            ))
            response.status_code = 404
            return response

        # Check if subcomment has been submitted by the same author
        subcomment_author = SubComment.query.filter_by(
            user_id=g.current_user['id'],
            sub_comment=subcomment_request['subcomment'].strip(),
            comment_id=subcomment_request['comment_id'].strip()
        ).first()

        if subcomment_author:
            response = jsonify(dict(
                data=dict(
                    message='Subcomment already exist'
                ),
                status='fail'
            ))
            response.status_code = 202
            return response

        new_subcomment = SubComment(
            id=PushID().next_id(),
            sub_comment=subcomment_request['subcomment'],
            comment=subcomment_comment,
            user=subcomment_poster
        )
        db.session.add(new_subcomment)
        db.session.commit()

        response = jsonify(dict(
            data=dict(
                message='Subcomment created successfully'
            ),
            status='success'
        ))
        response.status_code = 201
        return response

    @validate_token
    def get(self, subcomment_id=None):
        if subcomment_id is not None:
            subcomment = SubComment.query.filter_by(
                id=subcomment_id.strip()
            ).first()
            if not subcomment:
                response = jsonify(dict(
                    data=dict(
                        message='subcomment not Found'
                    ),
                    status='fail'
                ))
                response.status_code = 404
                return response

            response = jsonify(dict(
                data=dict(
                    id=subcomment.id,
                    subcomment=subcomment.sub_comment,
                    comment_id=subcomment.comment_id,
                    date=subcomment.created_at
                ),
                status='success'
            ))
            response.status_code = 200
            return response

        # subcomments = SubComment.query.all()
        response = jsonify(dict(
            data=dict(
                message='Bad request'
            ),
            status='fail'
        ))
        response.status_code = 403
        return response

    @validate_token
    def put(self, subcomment_id=None):

        if subcomment_id is not None:
            query_subcom = SubComment.query.filter_by(
                id=subcomment_id.strip(),
                user_id=g.current_user['id']
            ).first()

            if not query_subcom:
                response = jsonify(dict(
                    data=dict(
                        message='subcomment not found'
                    ),
                    status='fail'
                ))
                response.status_code = 404
                return response

            for i in ['subcomment']:
                if i not in request.get_json().keys():
                    response = jsonify(dict(
                        data=dict(
                            message='{} is required'.format(i)
                        ),
                        status='fail'
                    ))
                    response.status_code = 400
                    return response

                if request.get_json()[i].strip() == '':
                    response = jsonify(dict(
                        data=dict(
                            message='{} can not be empty'.format(i)
                        ),
                        status='fail'
                    ))
                    response.status_code = 400
                    return response

            query_subcom.sub_comment = request.get_json()['subcomment'].strip()
            db.session.commit()

            response = jsonify(dict(
                data=dict(
                    message='Subcomment updated successfully'
                ),
                status='fail'
            ))
            response.status_code = 200
            return response

        response = jsonify(dict(
            data=dict(
                message='Subcomment identity is required'
            ),
            status='fail'
        ))
        response.status_code = 403
        return response

    @validate_token
    def delete(self, subcomment_id=None):
        if subcomment_id is not None:
            subcomment = SubComment.query.filter_by(
                id=subcomment_id.strip(),
                user_id=g.current_user['id']
            ).first()
            if not subcomment:
                response = jsonify(dict(
                    data=dict(
                        message='subcomment not Found'
                    ),
                    status='fail'
                ))
                response.status_code = 404
                return response

            db.session.delete(subcomment)
            db.session.commit()
            response.status_code = 200
            return response
