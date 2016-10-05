import pathlib

_basedir = pathlib.Path(__file__).parents[1]

SQLALCHEMY_DATABASE_URI = (
    'sqlite:///' + str(_basedir.joinpath(pathlib.PurePath('app.db')).resolve())
)

SECRET_KEY = 'INSECURE'

MAIL_SERVER = 'localhost'
MAIL_PORT = '25'
MAIL_DEFAULT_SENDER = 'no-reply@localhost.localdomain'

del pathlib
