from setuptools import setup, find_packages

setup(
    name="IIS",
    version="0.0",
    long_description=__doc__,
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask>=0.11.1,<0.12.0",
        "Flask-Bootstrap>=3.3.7.0,<4.0.0.0",
        "Flask-Login>=0.3.2,<0.4.0",
        "Flask-Mail>=0.9.1,<0.10.0",
        "Flask-SQLAlchemy>=2.1,<3.0",
        "Flask-User>=0.6.8,<0.7.0",
        "Flask-WTF>=0.12,<0.13.0",
        "Flask-Migrate>=2.0.0,<3.0.0",
        "Flask-Testing>=0.6.1,<0.7.0",
        "daemonize>=2.4.7,<3.0.0"
    ],
    extras_require={
        'dev': [
            'mypy-lang>=0.4.4,<0.5.0'
        ]
    }
)
