INSTALLED = .installed

FLASK_APP = FLASK_APP=iis/__init__.py
IIS_FLASK_SETTINGS = IIS_FLASK_SETTINGS=../configuration/development.py

run-dev : $(INSTALLED)
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
