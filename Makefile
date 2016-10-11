CSS_MAIN = iis/static/css/iis_style.css
SCSS_MAIN = iis/static/sass/iis_style.scss
BOOTSTRAP_VER = 3.3.7

run-dev : install $(CSS_MAIN) js
	vex iis /bin/sh -c "IIS_FLASK_SETTINGS=../configuration/development.py \
	  ./run.py"

js : 
	-mkdir -p ./iis/static/js
	cp components/bootstrap-sass-$(BOOTSTRAP_VER)/assets/javascripts/bootstrap.js iis/static/js/


$(CSS_MAIN) : $(SCSS_MAIN)
	-mkdir -p ./iis/static/css
	sass --scss -I components/bootstrap-sass-$(BOOTSTRAP_VER)/assets/stylesheets/ \
	  $(SCSS_MAIN):$(CSS_MAIN)

install : .installed
	
.installed : setup.py
	vex iis pip install -e .[dev]
	touch .installed

.PHONY : clean
clean :
	find . -type f -name '*.pyc' -delete
	-find . -type d -name '__pycache__' -delete
	-rm -rf ./dist
	-rm -rf ./IIS.egg-info
	-rm .installed
	-rm -rf .sass-cache
