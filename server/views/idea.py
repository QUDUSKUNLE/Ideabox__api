from flask import g, jsonify, request
from flask_restful import Resource

from ..auth import validate_token
from ..middlewares import PushID
from ..model import User, Idea, Category, Tag, db


class IdeaResources(Resource):

    @validate_token
    def post(self):
        idea = request.get_json()
        for i in ['title', 'description', 'category_type', 'status']:
            if i not in idea.keys():
                response = jsonify(dict(
                    data=dict(
                        message='Idea {} is required'.format(i)
                    ),
                    status='fail'
                ))
                response.status_code = 401
                return response

            for i, v in idea.items():
                if idea[i].strip() == '':
                    response = jsonify(dict(
                        data=dict(
                            message='{} can not be empty'.format(i)
                        ),
                        status='fail'
                    ))
                    response.status_coe = 401
                    return response
        # Check if category_type exist
        category_creator = Category.query.filter_by(
            id=idea['category_type']
        ).first()
        if not category_creator:
            response = jsonify(dict(
                data=dict(
                    message='{} category is not found'.format(
                        idea['category_type']
                    )
                ),
                status='fail'
            ))
            response.status_code = 401
            return response

        # Check if idea title already exist
        check_idea = Idea.query.filter_by(title=idea['title'].strip()).first()
        if check_idea:
            response = jsonify(dict(
                data=dict(
                    message='Idea title already exist'
                ),
                status='fail'
            ))
            response.status_code = 409
            return response

        # Check if status is present
        check_status = Tag.query.filter_by(id=idea['status']).first()
        if not check_status:
            response = jsonify(dict(
                data=dict(
                    message='Idea status is invalid'
                ),
                status='fail'
            ))
            response.status_code = 401
            return response

        idea_creator = User.query.filter_by(id=g.current_user['id']).first()
        new_idea = Idea(
            id=PushID().next_id(),
            title=idea['title'].strip(),
            description=idea['description'].strip(),
            user=idea_creator,
            category=category_creator,
            tag=check_status
        )
        db.session.add(new_idea)
        db.session.commit()

        response = jsonify(dict(
            data=dict(
                id=new_idea.id,
                title=new_idea.title,
                user=new_idea.user.id,
                category=new_idea.category.id,
                description=new_idea.description
            ),
            message='Idea created successfully',
            status='success'
        ))
        response.status_code = 201
        return response

    @validate_token
    def get(self, idea_id=None):
        if idea_id is not None:
            idea = Idea.query.filter_by(id=idea_id).first()
            if not idea:
                response = jsonify(dict(
                    data=dict(
                        message='Idea not Found'
                    ),
                    status='fail'
                ))
                response.status_code = 404
                return response

            response = jsonify(dict(
                data=dict(
                    message=dict(
                        id=idea.id,
                        title=idea.title,
                        description=idea.description,
                        status=idea.idea_status,
                        user_id=idea.user_id,
                        category_id=idea.category_id,
                        created_at=idea.created_at
                    )
                ),
                status='success'
            ))
            response.status_code = 200
            return response

        user_ideas = Idea.query.filter(
            Idea.user_id == g.current_user['id']
        ).all()

        count = Idea.query.filter(
            Idea.user_id == g.current_user['id']
        ).count()
        if not user_ideas:
            response = jsonify(dict(
                data=dict(
                    message=[]
                ),
                status='success'
            ))
            response.status_code = 200
            return response

        response = jsonify(dict(
            data=dict(
                count=count,
                message=[dict(
                    id=idea.id,
                    title=idea.title,
                    description=idea.description,
                    status=idea.idea_status,
                    user_id=idea.user_id,
                    category_id=idea.category_id,
                    created_at=idea.created_at
                ) for idea in user_ideas]
            ),
            status='success',
        ))
        response.status_code = 200
        return response

    @validate_token
    def put(self, idea_id=None):
        for i in ['title', 'description', 'category_type', 'status']:
            if i not in request.get_json().keys():
                response = jsonify(dict(
                    data=dict(
                        message='Idea {} is required'.format(i)
                    ),
                    status='fail'
                ))
                response.status_code = 401
                return response

            for i, v in request.get_json().items():
                if request.get_json()[i].strip() == '':
                    response = jsonify(dict(
                        data=dict(
                            message='{} can not be empty'.format(i)
                        ),
                        status='fail'
                    ))
                    response.status_coe = 401
                    return response

        # Check if category_type exist
        category_creator = Category.query.filter_by(
            id=request.get_json()['category_type']
        ).first()
        if not category_creator:
            response = jsonify(dict(
                data=dict(
                    message='{} category is not found'.format(
                        request.get_json()['category_type'].strip()
                    )
                ),
                status='fail'
            ))
            response.status_code = 401
            return response

        # Check if idea title already exist
        check_idea = Idea.query.filter_by(
            title=request.get_json()['title'].strip()
        ).first()
        if check_idea:
            response = jsonify(dict(
                data=dict(
                    message='Idea title already exist'
                ),
                status='fail'
            ))
            response.status_code = 409
            return response

        # Check if status is present
        check_status = Tag.query.filter_by(
            id=request.get_json()['status'].strip()
        ).first()
        if not check_status:
            response = jsonify(dict(
                data=dict(
                    message='Idea status is invalid'
                ),
                status='fail'
            ))
            response.status_code = 401
            return response

        idea = Idea.query.filter_by(
            id=idea_id.strip(),
            user_id=g.current_user['id']
        ).first()
        if not idea:
            response = jsonify(dict(
                data=dict(
                    message='Idea not found'
                ),
                status='fail'
            ))
            response.status_code = 404
            return response

        idea.title = request.get_json()['title'].strip()
        idea.description = request.get_json()['description'].strip()
        db.session.commit()
        response = jsonify(dict(
            data=dict(
                message='Idea updated successfully'
            ),
            status='success'
        ))
        response.status_code = 205
        return response

    @validate_token
    def delete(self, idea_id=None):
        if idea_id is None:
            response = jsonify(dict(
                data=dict(
                    message='Unauthorized to perform this operation'
                ),
                status='fail'
            ))
            response.status_code = 401
            return response

        check_user = Idea.query.filter_by(
            id=idea_id.strip(),
            user_id=g.current_user['id']
        ).first()
        if not check_user:
            response = jsonify(dict(
                data=dict(
                    message='Idea not found'
                ),
                status='fail'
            ))
            response.status_code = 404
            return response

        db.session.delete(check_user)
        db.session.commit()
        response = jsonify(dict(
            data=dict(
                message='Idea deleted successfully'
            ),
            status='success'
        ))
        response.status_code = 202
        return response
