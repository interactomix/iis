import tempfile
from datetime import datetime

import flask_testing
from flask import url_for

import iis
from iis.models import User
from iis.extensions import db


class BaseTestCase(flask_testing.TestCase):
    DB_FILE = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DB_FILE[1]
    LOGGING = {"version": 1}
    TESTING = True
    WTF_CSRF_ENABLED = False
    USER_ENABLE_LOGIN_WITHOUT_CONFIRM = True

    def create_app(self):
        ret = iis.create_app(self.__class__)
        app = ret[0]
        self.user_manager = ret[1]
        return app

    def setUp(self):
        db.create_all()
        self.create_user("admin", "passW1")

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username=None, password=None):
        username = username or "admin"
        password = password or "passW1"
        self.client.post(url_for('user.login'), data=dict(
            username=username,
            password=password
        ), follow_redirects=False)
        return User.query.filter_by(username=username).one()

    def logout(self):
        self.client.get(url_for("user.logout"))

    def create_user(self, username, password):
        user = User(username=username,
                    password=self.user_manager.hash_password(password),
                    email=username + "@localhost",
                    confirmed_at=datetime.fromtimestamp(0.0),
                    active=True)
        db.session.add(user)
        db.session.commit()
        return user

    def assertLoginRequired(self, url):
        self.logout()

        res = self.client.get(url)
        self.assertEqual(302, res.status_code)
        self.assertIn(url_for('user.login'), res.headers['Location'])
