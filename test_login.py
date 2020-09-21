import unittest
import json
from app import app, db
from app.models import User
import ssl

class MyTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        app.config['WTF_CSRF_ENABLED'] = False  # close the csrf
        ssl._create_default_https_context = ssl._create_unverified_context
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_server(self):
        response = self.app.get('/')

    def test_register(self):
        # mock the data to register
        test_data = json.dumps(dict(email="xxx@xxx.com", type="password", password="123"))

        # post data
        response = self.app.post('/api/signup', data=test_data)

        # register at first time, it should be successful
        assert '201' in response.status

        # find data if exist in database
        result = db.session.query(User)
        assert result.first().email == "xxx@xxx.com"

        # # register second time, it should be refused
        # response = self.app.post('/api/signup', data=test_data)
        # assert '400' in response.status

    def test_login(self):
        # register a user and login

        # mock register
        test_data = json.dumps(dict(email="xxx@xxx.com", type="password", password="123"))
        response = self.app.post('/api/signup', data=test_data)
        assert '201' in response.status
        result = db.session.query(User).first()
        result.confirmed = True
        db.session.commit()

        # login
        test_data = json.dumps(dict(email="xxx@xxx.com", type="password", password="123"))
        response = self.app.post('/api/login', data=test_data)

        assert '200' in response.status

        # invalid username
        invalid_data = json.dumps(dict(email="yyy@xxx.com", type="password", password="456"))
        response = self.app.post('/api/login', data=invalid_data)

        assert '403' in response.status



if __name__ == '__main__':
    unittest.main()
