import flask
import flask_user
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from . import jobs, models, forms
from ..extensions import csrf, db


@csrf.exempt
@jobs.route("/", methods=["GET"])
def search():
    form = forms.SearchForm(flask.request.args, csrf_enabled=False)
    if form.validate():
        defs = models.PipelineDefinition.query.filter(
            models.PipelineDefinition.name.like(
                "%" + form.search_term.data + "%"
            )
        )
    else:
        defs = models.PipelineDefinition.query.limit(10)

    return flask.render_template("jobs/search.html", form=form, defs=defs)


@jobs.route("/upload", methods=["GET", "POST"])
@flask_user.login_required
def upload():
    form = forms.JobForm(flask.request.form)
    form.user_id.data = current_user.get_id()
    if flask.request.method == "POST" and form.validate():
        definition = models.PipelineDefinition()
        form.populate_obj(definition)
        definition.user = current_user

        db.session.add(definition)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise
        else:
            return flask.redirect(flask.url_for('jobs.search'))

    return flask.render_template("jobs/upload.html", form=form)


@jobs.route("/<int:job_id>", methods=["GET", "POST"])
def detail(job_id):
    job = models.PipelineDefinition.query.get(job_id)
    if job is None:
        return flask.abort(404)

    if flask.request.method == "POST":
        if current_user != job.user:
            return flask.redirect(flask.url_for("jobs.detail", job_id=job_id))

        form = forms.JobForm(flask.request.form, id=job.id)
        form.user_id.data = current_user.get_id()
        if form.validate():
            form.populate_obj(job)
            db.session.add(job)
            db.session.commit()
            flask.flash('The job "' + job.name + '" was successfully updated')
            return flask.redirect(flask.url_for("jobs.detail", job_id=job_id))

        return flask.render_template("jobs/detail.html", form=form,
                                     disabled=False)

    if flask.request.method == "GET":
        form = forms.JobForm(obj=job)
        disabled = True
        if current_user == job.user:
            disabled = False

        return flask.render_template("jobs/detail.html", form=form,
                                     disabled=disabled)
