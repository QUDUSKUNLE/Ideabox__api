import os

from flask_testing import TestCase
from server.model import db
from main import app_config


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        self.app = app_config(os.environ.get('TEST_ENVIRONMENT'))
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        return self.app

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
