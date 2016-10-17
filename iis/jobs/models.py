from typing import Any  # noqa: F401

import flask.current_app

db = flask.current_app.config["jobs.db"]
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
