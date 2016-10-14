import json

import flask_wtf
import wtforms.fields
from wtforms import validators

from . import models


def is_json(form, field):
    try:
        json.loads(field.data)
    except (ValueError, TypeError):
        raise validators.ValidationError('The field must contain valid JSON.')


class SearchForm(flask_wtf.Form):
    search_term = wtforms.fields.StringField()


class CreateForm(flask_wtf.Form):
    name = wtforms.fields.StringField()
    user_id = wtforms.fields.IntegerField()
    description = wtforms.fields.TextAreaField()
    public = wtforms.fields.BooleanField()
    definition = wtforms.fields.TextAreaField(
        "Pipeline Definition", [is_json])

    def validate(self):
        valid = super().validate()
        if not valid:
            return valid

        definition = models.PipelineDefinition.query.filter(
            models.PipelineDefinition.name == self.name.data,
            models.PipelineDefinition.user_id == self.user_id.data
        ).first()
        if definition:
            self.name.errors.append("The name must be unique.")
            return False
        else:
            return True
