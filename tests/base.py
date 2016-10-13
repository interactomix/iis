import tempfile

import flask_testing
from flask_login import login_user, logout_user
from flask import url_for

import iis
from iis.models import User
from iis.database import db


class BaseTestCase(flask_testing.TestCase):
    DB_FILE = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DB_FILE[1]
    LOGGING = {"version": 1}

    def create_app(self):
        app = iis.create_app(self.__class__)
        return app

    def setUp(self):
        db.create_all()
        admin = User(username="admin", password="passW1",
                     email="admin@localhost")
        db.session.add(admin)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username):
        user = User.query.filter_by(username=username).one()
        login_user(user)

    def logout(self):
        logout_user()

    def assertLoginRequired(self, url):
        try:
            logout_user()
        except:
            pass

        res = self.client.get(url)
        self.assertEqual(302, res.status_code)
        self.assertIn(url_for('user.login'), res.headers['Location'])
