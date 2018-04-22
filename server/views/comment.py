from flask import g, jsonify, request
from flask_restful import Resource

from ..auth import validate_token
from ..middlewares import PushID
from ..model import User, Idea, Comment, SubComment, db


class CommentResource(Resource):

    @validate_token
    def post(self):
        comment_request = request.get_json()
        for key in ['idea_id', 'comment']:
            if key not in request.get_json().keys():
                response = jsonify(dict(
                    data=dict(
                        message='{} is required'.format(key)
                    ),
                    status='fail'
                ))
                response.status_code = 404
                return response

            if (request.get_json()[key]).strip() == '':
                response = jsonify(dict(
                    data=dict(
                        message='{} value cannot be empty'.format(key)
                    ),
                    status='fail'
                ))
                response.status_code = 404
                return response

        comment_creator = User.query.filter_by(id=g.current_user['id']).first()
        if not comment_creator:
            response = jsonify(dict(
                data=dict(
                    message='User not Found'
                ),
                status='fail'
            ))
            response.status_code = 404
            return response

        idea_comment = Idea.query.filter_by(
            id=comment_request['idea_id']
        ).first()
        if not idea_comment:
            response = jsonify(dict(
                data=dict(
                    message='Idea not Found'
                ),
                status='fail'
            ))
            response.status_code = 404
            return response
        # Check if the comment already exist with the same
        comment_check = Comment.query.filter_by(
            user_id=g.current_user['id'],
            comment=request.get_json()['comment'].strip(),
            idea_id=request.get_json()['idea_id'].strip()
        ).first()

        if comment_check:
            response = jsonify(dict(
                data=dict(
                    message='Comment already exist'
                ),
                status='fail'
            ))
            response.status_code = 409
            return response

        new_comment = Comment(
            id=PushID().next_id(),
            comment=comment_request['comment'],
            user=comment_creator,
            idea=idea_comment
        )
        db.session.add(new_comment)
        db.session.commit()

        response = jsonify(
            dict(
                data=dict(
                    message='Comment created successfully'
                ),
                status='success'
            )
        )
        response.status_code = 201
        return response

    @validate_token
    def get(self):
        comments = Comment.query.all()
        response = jsonify(dict(
            data=[
                dict(
                    id=comment.id,
                    comment=comment.comment,
                    idea_id=comment.idea_id,
                    user_id=comment.user_id,
                    date=comment.created_at
                ) for comment in comments
            ],
            status='success'
        ))
        response.status_code = 200
        return response

    @validate_token
    def put(self, comment_id=None):
        if comment_id is None:
            response = jsonify(dict(
                data=dict(
                    message='Bad request'
                ),
                status='fail'
            ))
            response.status_code = 403
            return response

        query_comment = Comment.query.filter_by(
            id=comment_id.strip(),
            user_id=g.current_user['id']
        ).first()

        if not query_comment:
            response = jsonify(dict(
                data=dict(
                    message='Comment not found'
                ),
                status='fail'
            ))
            response.status_code = 404
            return response

        query_comment.comment = request.get_json()['comment']
        db.session.commit()
        response = jsonify(dict(
            data=dict(
                message='Comment update successfully'
            ),
            status='success'
        ))
        response.status_code = 202
        return response

    @validate_token
    def delete(self, comment_id=None):
        if comment_id is None:
            response = jsonify(dict(
                data=dict(
                    message='Bad request'
                ),
                status='fail'
            ))
            response.status_code = 403
            return response

        query_comment = Comment.query.filter_by(
            id=comment_id.strip(),
            user_id=g.current_user['id']
        ).first()

        if not query_comment:
            response = jsonify(dict(
                data=dict(
                    message='Bad request'
                ),
                status='fail'
            ))
            response.status_code = 403
            return response

        query_subcomments = SubComment.query.filter_by(
            comment_id=comment_id
        ).all()
        for query_subcomment in query_subcomments:
            db.session.delete(query_subcomment)

        db.session.delete(query_comment)
        db.session.commit()

        response = jsonify(dict(
            data=dict(
                message='Comment deleted successfully'
            ),
            status='fail'
        ))
        response.status_code = 200
        return response
