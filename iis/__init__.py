import logging.config

from flask import Flask
from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from flask_migrate import Migrate


def create_app(config: object) -> Flask:
    """Create the flask app. Can be called from testing contexts"""
    app = Flask(__name__)
    app.config.from_envvar("IIS_FLASK_SETTINGS")
    app.config.from_object(config)

    # Register blueprints
    from iis.jobs import jobs
    app.register_blueprint(jobs, url_prefix="/jobs")

    # Init db
    from .database import db
    db.init_app(app)

    from .models import User
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)  # noqa: F841
    Migrate(app, db)

    # Call app.logger to prevent it from clobbering configuration
    app.logger
    logging.config.dictConfig(app.config["LOGGING"])
    app.logger.info("App configured.")
    return (app, user_manager)

app = create_app(None)[0]

# Load Flask-Mail
mail = Mail(app)

from iis import views  # noqa: E402, F401
