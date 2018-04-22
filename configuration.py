import os
from dotenv import load_dotenv
from os.path import join

dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

def app_config(app):
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'SQLALCHEMY_DATABASE_URI'
    )
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
