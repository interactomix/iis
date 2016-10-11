from typing import Any  # noqa: F401

from iis.database import db

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
    db.UniqueConstraint('user_id', 'name')
