from typing import Any  # noqa: F401
import datetime

from ..extensions import db

Model = db.Model  # type: Any


class PipelineDefinition(Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    definition = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User', backref=db.backref('pipeline_definitions', lazy='dynamic')
    )
    public = db.Column(db.Boolean)
    __table_args__ = (db.UniqueConstraint('user_id', 'name'),)


class CreateJobProgress(Model):
    @classmethod
    def current_time(cls) -> datetime.datetime:
        return datetime.datetime.now()

    id = db.Column(db.Integer, primary_key=True)

    progress = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    user = db.relationship(
        "User", backref=db.backref("CreateJobProgress", lazy="dynamic")
    )
    last_edited = db.Column(db.DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)

