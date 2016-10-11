import flask
import flask_user
import flask_login

from . import jobs, models, forms
import iis.forms


@jobs.route("/create", methods=["GET", "POST"])
@flask_user.login_required
def create():
    if flask.request.method == "GET":
        form = iis.forms.process_selection_form()()
        return flask.render_template("jobs/create.html", form=form)


@jobs.route("/", methods=["GET"])
def search_definitions():
    form = forms.PipelineDefinitionSearchForm()
    if form.validate_on_submit():
        defs = models.Definition.query.filter(
            models.PipelineDefinition.user_id == flask_login.current_user.id,
            models.PipelineDefinition.title.like("%" + form.search_term + "%")
        )
    else:
        defs = models.PipelineDefinition.query.filter(
            models.PipelineDefinition.user_id == flask_login.current_user.id
        )

    print(defs)
    return flask.render_template("jobs/search.html", form=form, defs=defs)
