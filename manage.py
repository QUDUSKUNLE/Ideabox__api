import os

from flask import jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_migrate import Migrate
from flask_script import Manager
from dotenv import load_dotenv
from os.path import join
from server.model import app, db
from config import development_environment
from server.views import (
    NewUserResources, UserResources, ResetPasswordResources,
    IdeaResources, CategoryResources, TagResources, CommentResource,
    SubCommentResource
)

dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

def app_config(app, environment):
    app.config['DEBUG'] = environment['DEBUG']
    app.config['SQLALCHEMY_DATABASE_URI'] = environment['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_ECHO'] = environment['SQLALCHEMY_ECHO']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = environment['SQLALCHEMY_TRACK_MODIFICATIONS']
    app.config['SECRET_KEY'] = environment['SECRET_KEY']
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = environment['JSONIFY_PRETTYPRINT_REGULAR']

    # Cross Origin Resource
    CORS(app)

    # initialize SQLAlchemy
    db.init_app(app)
        
    Manager(app)

    Migrate(app, db)

    # initilize api resources
    api = Api(app)


    @app.route('/')
    def index():
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

if __name__ == '__main__':
    manager = app_config(app, development_environment)
    manager.run()
