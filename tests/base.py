import tempfile
from datetime import datetime

import flask_testing
from flask import url_for
from flask_login import current_user

import iis
from iis.models import User
from iis.database import db


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
        admin = User(username="admin",
                     password=self.user_manager.hash_password("passW1"),
                     email="admin@localhost",
                     confirmed_at=datetime.fromtimestamp(0.0),
                     active=True)
        db.session.add(admin)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username=None, password=None):
        self.client.post(url_for('user.login'), data=dict(
            username=username or "admin",
            password=password or "passW1"
        ), follow_redirects=False)
        # self.assertEqual(current_user.username, "admin")

    def logout(self):
        self.client.get(url_for("user.logout"))

    def assertLoginRequired(self, url):
        self.logout()

        res = self.client.get(url)
        self.assertEqual(302, res.status_code)
        self.assertIn(url_for('user.login'), res.headers['Location'])
