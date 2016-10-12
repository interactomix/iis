import flask
import flask_user
from flask_login import current_user

from iis.database import db
import iis.forms
from . import jobs, models, forms


@jobs.route("/create", methods=["GET", "POST"])
@flask_user.login_required
def create():
    if flask.request.method == "GET":
        form = iis.forms.process_selection_form()()
        return flask.render_template("jobs/create.html", form=form)


@jobs.route("/", methods=["GET"])
def search_definitions():
    form = forms.SearchForm()
    if current_user.is_anonymous:
        if form.validate_on_submit():
            defs = models.Definition.query.filter(
                models.PipelineDefinition.title.like(
                    "%" + form.search_term + "%"
                )
            )
        else:
            defs = models.PipelineDefinition.query.limit(10)

    else:
        if form.validate_on_submit():
            defs = models.Definition.query.filter(
                models.PipelineDefinition.user_id == current_user.id,
                models.PipelineDefinition.title.like(
                    "%" + form.search_term + "%"
                )
            )
        else:
            defs = models.PipelineDefinition.query.filter(
                models.PipelineDefinition.user_id == current_user.id
            )

    print(defs)
    return flask.render_template("jobs/search.html", form=form, defs=defs)


@jobs.route("/upload", methods=["GET", "POST"])
@flask_user.login_required
def upload():
    form = forms.UploadForm()
    if form.validate_on_submit():
        definition = models.PipelineDefinition(
            name=form.name,
            description=form.description,
            definition=form.file.data.read(),
            user_id=current_user.id,
            public=form.publish,
        )
        db.session.add(definition)
        db.session.commit()

    return flask.render_template("jobs/upload.html", form=form)
