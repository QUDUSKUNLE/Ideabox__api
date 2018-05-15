import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from server.model import db
from server.views import (
    NewUserResources, UserResources, ResetPasswordResources,
    IdeaResources, CategoryResources, TagResources, CommentResource,
    SubCommentResource
)

import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def app_config(environment):
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_object(environment)

    # Cross Origin Resource
    CORS(app)

    # initialize SQLAlchemy
    db.init_app(app)
        
    # initilize api resources
    api = Api(app)


    @app.route('/')
    def home():
        return jsonify({'message': 'Welcome to Ideabox'}), 200


    # Sign up resource
    api.add_resource(
        NewUserResources,
        '/api/v1/signup',
        '/api/v1/signup/',
        endpoint='signup'
    )

    # Sign in resource
    api.add_resource(
        UserResources,
        '/api/v1/signin',
        '/api/v1/signin/',
        endpoint='signin'
    )

    api.add_resource(
        ResetPasswordResources,
        '/api/v1/resetpassword',
        '/api/v1/resetpassword/',
        endpoint='resetpassword'
    )

    api.add_resource(
        IdeaResources,
        '/api/v1/idea',
        '/api/v1/idea/',
        '/api/v1/idea/<string:idea_id>',
        '/api/v1/idea/<string:idea_id>/',
        endpoint='idea'
    )

    api.add_resource(
        CategoryResources,
        '/api/v1/category',
        '/api/v1/category/',
        '/api/v1/category/<string:category_id>',
        '/api/v1/category/<string:category_id>/',
        endpoint='category'
    )

    api.add_resource(
        TagResources,
        '/api/v1/tag',
        '/api/v1/tag/',
        endpoint='tag'
    )

    api.add_resource(
        CommentResource,
        '/api/v1/comment',
        '/api/v1/comment/',
        '/api/v1/comment/<string:comment_id>',
        '/api/v1/comment/<string:comment_id>/',
        endpoint='comment'
    )

    api.add_resource(
        SubCommentResource,
        '/api/v1/subcomment',
        '/api/v1/subcomment/',
        '/api/v1/subcomment/<string:subcomment_id>',
        '/api/v1/subcomment/<string:subcomment_id>/',
        endpoint='subcomment'
    )
    return app

app = app_config(os.environ.get('ENVIRONMENT'))

if __name__ == '__main__':
    app = app_config(os.environ.get('ENVIRONMENT'))
    app.run()
