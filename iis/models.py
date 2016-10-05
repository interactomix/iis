from typing import Any  # noqa: F401

from flask_user import UserMixin

from iis import db

Model = db.Model  # type: Any


class User(Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100),
                                     nullable=False,
                                     server_default='')

    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    active = db.Column('is_active',
                       db.Boolean(),
                       nullable=False,
                       server_default='0')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')


class Computation(Model):
    id = db.Column(db.Integer, primary_key=True)

    process_uid = db.Column(db.String(100), nullable=False, unique=True)
    pdf = db.Column(db.Text(), nullable=True, unique=False)
    input_data = db.Column(db.Text())
    output_data = db.Column(db.Text())
    status = db.Column(db.Enum("processing",
                               "interrupted",
                               "finished",
                               "stopped"))
    progress = db.Column(db.Integer())
