import logging.config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from flask_bootstrap import Bootstrap


def create_app(config: object) -> Flask:
    """Create the flask app. Can be called from testing contexts"""
    app = Flask(__name__)
    app.config.from_envvar('IIS_FLASK_SETTINGS')
    app.config.from_object(config)

    # Call app.logger to prevent it from clobbering configuration
    app.logger
    logging.config.dictConfig(app.config['LOGGING'])
    app.logger.info("App configured.")
    return app

app = create_app(None)

# Set up SQLAlchemy and Migrate
db = SQLAlchemy(app)  # type: SQLAlchemy
migrate = Migrate(app, db)

# Load Flask-Mail
mail = Mail(app)

# Set up bootstrap
Bootstrap(app)

# Configure user model for Flask-User
from iis.models import User  # noqa: E402

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)



from iis import views, models  # noqa: E402, F401
