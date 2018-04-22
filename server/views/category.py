from flask import jsonify, request
from flask_restful import Resource

from ..auth import validate_token
from ..middlewares import PushID
from ..model import Category, db


class CategoryResources(Resource):

    @validate_token
    def post(self):
        category = request.get_json()

        for i in ['category_type']:
            if i not in category.keys():
                response = jsonify(dict(
                    data=dict(
                        message='{} is required'.format(i)
                    ),
                    status='fail'
                ))

                response.status_code = 401
                return response

            for i, v in category.items():
                if category[i].strip() == '':
                    response = jsonify(dict(
                        data=dict(
                            message='{} can not be empty'.format(i)
                        ),
                        status='fail'
                    ))
                    response.status_code = 401
                    return response

        # Check if category already exist
        category_type = Category.query.filter_by(
            category_type=category['category_type'].strip()
        ).first()
        if category_type:
            response = jsonify(dict(
                data=dict(
                    message='Category type already exist'
                ),
                status='fail'
            ))
            response.status_code = 409
            return response

        new_category = Category(
            id=PushID().next_id(),
            category_type=category['category_type'].strip()
        )
        db.session.add(new_category)
        db.session.commit()

        response = jsonify(dict(
            data=dict(
                message='Category created successfully'
            ),
            status='success'
        ))
        response.status_code = 201
        return response

    @validate_token
    def get(self, category_id=None):
        if category_id is not None:
            category = Category.query.filter_by(id=category_id).first()
            if not category:
                response = jsonify(dict(
                    data=dict(
                        message='Category does not exist'
                    ),
                    status='fail'
                ))
                response.status_code = 401
                return response

            return jsonify(dict(
                category_id=category.id,
                category_type=category.category_type
            ))

        all_category = Category.query.all()
        count = Category.query.count()
        return jsonify(dict(
            data=dict(
                message=[
                    dict(
                        category_id=category.id,
                        category_type=category.category_type
                    ) for category in all_category
                ],
                count=count
            ),
            status='success',
        ))
