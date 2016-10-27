from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask_assets import Environment

db = SQLAlchemy()
csrf = CsrfProtect()
assets = Environment()
