from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config')

# Set up SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Load Flask-Mail
mail = Mail(app)

# Set up bootstrap
Bootstrap(app)

# Configure user model for Flask-User
from app.models import User  # noqa: E402

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)


from app import views, models  # noqa: E402, F401
