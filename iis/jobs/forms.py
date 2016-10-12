import json

import flask_wtf
import wtforms.fields
from wtforms import validators


def is_json(form, field):
    try:
        json.loads(field.data)
    except ValueError:
        raise validators.ValidationError('The file must contain valid JSON.')


class SearchForm(flask_wtf.Form):
    search_term = wtforms.fields.StringField()


class UploadForm(flask_wtf.Form):
    name = wtforms.fields.StringField()
    description = wtforms.fields.TextAreaField()
    public = wtforms.fields.BooleanField()
    definition = wtforms.fields.TextAreaField(
        "Pipeline Definition", [is_json])
