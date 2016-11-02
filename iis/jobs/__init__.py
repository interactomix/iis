from flask import Blueprint

from .api import api


jobs = Blueprint('jobs', __name__,
                 template_folder='./templates')  # type: Blueprint

api.init_app(jobs)

from . import views, models # noqa: E402, F401
