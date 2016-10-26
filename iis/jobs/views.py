import json

import flask
import flask_user
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from . import jobs, models, forms, utils
from ..extensions import csrf, db


@jobs.route("/create", methods=["GET", "POST"])
@flask_user.login_required
def create():
    progress_query = models.CreateJobProgress.query.filter_by(
        user=current_user
    )
    if flask.request.method == "GET":
        if not progress_query.count():
            return flask.render_template("jobs/create_initial.html",
                                         form=forms.DataTypeForm())
        else:
            progress = progress_query.one()
            form = forms.CreateForm()
            form.next_process.choices = utils.get_choices(
                json.loads(progress.progress)
            )
            return flask.render_template("jobs/create.html", form=form)

    else:
        if "data_type" in flask.request.form:
            form = forms.DataTypeForm(flask.request.form)
            if not progress_query.count():
                if not form.validate():
                    return flask.render_template("jobs/create_initial.html",
                                                 form=form)
                else:
                    so_far = dict(
                        input={"quantity": form.quantity.data,
                               "type": form.data_type.data},
                        processes=[]
                    )
                    progress = models.CreateJobProgress()
                    progress.user = current_user
                    progress.progress = json.dumps(so_far)
                    db.session.add(progress)
                    db.session.commit()
                    main_form = forms.CreateForm()
                    main_form.next_process.choices = utils.get_choices(so_far)
                    return flask.render_template("jobs/create.html",
                                                 form=main_form)
            else:
                # This shouldn't happen!  Flash an error and redirect to
                # itself.
                flask.flash("You have unsaved progress in the database. " +
                            "You can continue with that, or explicitly reset "
                            "it.")
                return flask.redirect(flask.url_for("jobs.create"))
                
        else:
            if not progress_query.count():
                # This shouldn't happen! Flash an error and redirect
                flask.flash("You do not have any progress in the database. " +
                            "You must start the job creation process from "
                            "scratch!")
                return flask.redirect(flask.url_for("jobs.create"))
            else:
                progress = progress_query.one()
                so_far = json.loads(progress.progress)
                form = forms.CreateForm(flask.request.form)
                form.next_process.choices = utils.get_choices(so_far)
                if form.validate():
                    so_far["processes"].append({
                        "type": form.next_process.data
                    })
                    progress.progress = json.dumps(so_far)
                    db.session.add(progress)
                    db.session.commit()
                    main_form = forms.CreateForm()
                    main_form.next_process.choices = utils.get_choices(so_far)
                    return flask.render_template("jobs/create.html",
                                                 form=main_form)
                else:
                    return flask.render_template("jobs/create.html", form=form)


@csrf.exempt
@jobs.route("/", methods=["GET"])
def search():
    form = forms.SearchForm(flask.request.args, csrf_enabled=False)
    if form.validate():
        if form.search_description.data:
            defs = models.PipelineDefinition.query.filter(or_(
                models.PipelineDefinition.name.like(
                    "%" + form.search_term.data + "%",
                ),
                models.PipelineDefinition.description.like(
                    "%" + form.search_term.data + "%"
                )
            ))
        else:
            defs = models.PipelineDefinition.query.filter(
                models.PipelineDefinition.name.like(
                    "%" + form.search_term.data + "%",
                ),
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
