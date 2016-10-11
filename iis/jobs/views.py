import flask
from flask_user import login_required

from . import jobs
import iis.forms


@jobs.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if flask.request.method == "GET":
        form = iis.forms.process_selection_form()()
        return flask.render_template("jobs/create.html", form=form)
