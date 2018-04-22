import unittest
import os
import json

from server.model import db, app
from dotenv import load_dotenv
from os.path import join, dirname


class TestIdea(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        app.config['TESTING'] = True
        app.config['DEUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + Config.BASE_DIR \
            + '/test/test_db.sqlite'
        cls.app = app.test_client()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        response = self.app.get('/', follow_redirects=True)
        # self.assertEqual(response.status_code, 200)
        # self.assertIn('Welcome to Our World!', str(response.data))
        # self.assertIn('true', str(response.data))

    # def test_register(self):
    #     response = self.app.post('/register',
    #                              data=json.dumps(
    #                                  dict(name='quduskunle', password='kunle')),
    #                              content_type='application/json')
    #     self.assertEqual('New user created',
    #                      json.loads(response.data)['message'])
    #     self.assertEqual('quduskunle', json.loads(
    #         response.data)['user']['name'])
    #     self.assertEqual(response.status_code, 201)

    # def test_no_data(self):
    #     response = self.app.post('/register',
    #                              data=json.dumps(dict()), content_type='application/json')
    #     self.assertTrue(response.status_code == 403)
    #     self.assertEqual(json.loads(response.data)[
    #                      'message'], 'Invalid request')

    # def test_no_name(self):
    #     response = self.app.post('/register',
    #                              data=json.dumps(
    #                                  dict(name='', password='kola')),
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(json.loads(response.data)['message'],
    #                      'Either name or password cannot be empty')

    # def test_name(self):
    #     response = self.app.post('/login',
    #                              data=json.dumps(
    #                                  dict(name='kunle', password='kola')),
    #                              content_type='application/json'
    #                              )
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(json.loads(response.data)[
    #                      'message'], 'User not found')

    # def test_password(self):
    #     response = self.app.post('/login',
    #                              data=json.dumps(
    #                                  dict(name='quduskunle', password='kola')),
    #                              content_type='application/json')
    #     print(json.loads(response.data))
    #     # self.assertEqual(response.status_code, 401)
    #     # self.assertEqual(
    #     #     json.loads(response.data)['message'],
    #     #     'Incorrect username or password')

    # def test_get_user(self):
    #     response = self.app.get('/users', follow_redirects=True)
    #     #print(json.loads(response.data))


if __name__ == '__main__':
    unittest.main()
