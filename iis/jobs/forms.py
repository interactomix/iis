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
    search_term = wtforms.fields.StringField(
        validators=[validators.Optional()],
        default=""
    )
    search_description = wtforms.fields.BooleanField(
        default=False,
        description=("Descriptions of jobs will be searched if this option " +
                     "is checked.")
    )


class JobForm(flask_wtf.Form):
    name = wtforms.fields.StringField()
    user_id = wtforms.fields.IntegerField()
    description = wtforms.fields.TextAreaField()
    public = wtforms.fields.BooleanField()
    definition = wtforms.fields.TextAreaField(
        "Pipeline Definition", [is_json])

    def __init__(self, *args, **kwargs):
        self._id = kwargs.pop('id', None)
        super().__init__(*args, **kwargs)

    def validate(self):
        valid = super().validate()
        if not valid:
            return valid

        if self._id is not None:
            definition = models.PipelineDefinition.query.filter(
                models.PipelineDefinition.name == self.name.data,
                models.PipelineDefinition.user_id == self.user_id.data,
                models.PipelineDefinition.id != self._id
            ).first()
        else:
            definition = models.PipelineDefinition.query.filter(
                models.PipelineDefinition.name == self.name.data,
                models.PipelineDefinition.user_id == self.user_id.data
            ).first()

        if definition:
            self.name.errors.append("The name must be unique.")
            return False
        else:
            return True
