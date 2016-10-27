CSS_MAIN = iis/static/css/iis_style.css
SCSS_MAIN = iis/static/sass/iis_style.scss

BOOTSTRAP_SASS = ./iis/static/bower_components/bootstrap-sass/assets/stylesheets/
BOOTSTRAP_JS = ./iis/static/bower_components/bootstrap-sass/assets/javascripts/bootstrap.js

INSTALLED = .installed

FLASK_APP = FLASK_APP=iis/__init__.py
IIS_FLASK_SETTINGS = IIS_FLASK_SETTINGS=../configuration/development.py

run-dev : $(INSTALLED) $(CSS_MAIN)
	vex iis /bin/sh -c \
	  "$(IIS_FLASK_SETTINGS) \
	  FLASK_DEBUG=1 \
	  $(FLASK_APP) \
	  flask run"

test : $(INSTALLED)
	vex iis /bin/sh -c \
	  "$(IIS_FLASK_SETTINGS) \
	  python -m unittest"

mypy : $(INSTALLED)
	-vex iis /bin/sh -c \
	  "mypy -s -p iis"

css-watch : $(CSS_MAIN)
	sass --scss --watch -I $(BOOTSTRAP_SASS) $(SCSS_MAIN):$(CSS_MAIN)

$(CSS_MAIN) : $(SCSS_MAIN) $(BOOTSTRAP_SASS)_bootstrap.scss \
	      $(BOOTSTRAP_SASS)_bootstrap-sprockets.scss
	-mkdir -p ./iis/static/css
	sass --scss -I $(BOOTSTRAP_SASS) $(SCSS_MAIN):$(CSS_MAIN)

install: $(INSTALLED)

$(INSTALLED) : setup.py package.json
	vex iis pip install -e .[dev]
	npm install
	./node_modules/bower/bin/bower install
	touch $(INSTALLED)

.PHONY : clean clean-all migrate
clean :
	find . -type f -name '*.pyc' -delete
	-find . -type d -name '__pycache__' -delete
	-rm -rf ./dist
	-rm -rf ./IIS.egg-info
	-rm .installed
	-rm -rf .sass-cache

clean-components : 
	-rm -rf ./node_modules
	-rm -rf ./iis/static/bower_components

clean-all : clean clean-components

migrate : 
	vex iis /bin/sh -c \
	  "$(FLASK_APP) \
	  $(IIS_FLASK_SETTINGS) \
	  flask db migrate"

upgrade : 
	vex iis /bin/sh -c \
	  "$(FLASK_APP) \
	  $(IIS_FLASK_SETTINGS) \
	  flask db upgrade"
