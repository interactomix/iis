import tempfile

import flask_testing

import iis
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
