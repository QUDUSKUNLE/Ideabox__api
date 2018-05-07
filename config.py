import os
from dotenv import load_dotenv
from os.path import join

dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

development_environment = {
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': os.environ.get('SQLALCHEMY_DATABASE_URI'),
    'SQLALCHEMY_ECHO': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'SECRET_KEY': os.environ.get('SECRET_KEY'),
    'JSONIFY_PRETTYPRINT_REGULAR': True
}

test_environment = {
    'DEBUG': True,
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': os.environ.get('SQLALCHEMY_DATABASE_URI_TEST'),
    'SQLALCHEMY_ECHO': False,
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'SECRET_KEY': os.environ.get('SECRET_KEY'),
    'JSONIFY_PRETTYPRINT_REGULAR': False
}
