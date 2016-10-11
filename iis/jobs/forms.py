import flask_wtf
import wtforms.fields


class PipelineDefinitionSearchForm(flask_wtf.Form):
    search_term = wtforms.fields.StringField()
