import flask_wtf
import wtforms.fields


class SearchForm(flask_wtf.Form):
    search_term = wtforms.fields.StringField()


class UploadForm(flask_wtf.Form):
    name = wtforms.fields.StringField()
    description = wtforms.fields.TextAreaField()
    publish = wtforms.fields.BooleanField()
    definition = wtforms.fields.FileField()
