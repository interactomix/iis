import os
_basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')

SECRET_KEY = 'INSECURE'

MAIL_SERVER = 'localhost'
MAIL_PORT = '25'
MAIL_DEFAULT_SENDER = 'no-reply@localhost.localdomain'

del os
