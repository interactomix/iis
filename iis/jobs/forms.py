import json

from flask_login import current_user
import flask_wtf
import wtforms.fields
from wtforms import validators

from . import models


def is_json(form, field):
    try:
        json.loads(field.data)
    except ValueError:
        raise validators.ValidationError('The file must contain valid JSON.')


class SearchForm(flask_wtf.Form):
    search_term = wtforms.fields.StringField()


class CreateForm(flask_wtf.Form):
    name = wtforms.fields.StringField()
    description = wtforms.fields.TextAreaField()
    public = wtforms.fields.BooleanField()
    definition = wtforms.fields.TextAreaField(
        "Pipeline Definition", [is_json])

    def validate(self):
        valid = super().validate()
        if not valid:
            return valid

        if models.PipelineDefinition.query.filter_by(name=self.name.data,
                                                     user=current_user):
            self.name.errors.append("The name must be unique.")
            return False
