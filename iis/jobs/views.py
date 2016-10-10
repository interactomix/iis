import flask
from flask_user import login_required

from . import jobs
import iis.forms


@login_required
@jobs.route("/create", methods=["GET", "POST"])
def create():
    if flask.request.method == "GET":
        form = iis.forms.process_selection_form()()
        return flask.render_template("jobs/create.html", form=form)
