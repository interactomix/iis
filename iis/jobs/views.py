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
def search():
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
    if flask.request.method == "POST" and form.validate_on_submit():
        definition = models.PipelineDefinition()
        form.populate_obj(definition)
        definition.user = current_user

        db.session.add(definition)
        db.session.commit()

        return flask.redirect(flask.url_for('jobs.search'))

    return flask.render_template("jobs/upload.html", form=form)
