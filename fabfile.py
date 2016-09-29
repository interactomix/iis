from fabric.api import env, local

env.user = 'max'
env.hosts = ['localhost']


def pack():
    local('python setup.py sdist --formats=gztar', capture=False)
