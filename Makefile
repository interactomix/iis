run-dev : install css js
	vex iis /bin/sh -c "IIS_FLASK_SETTINGS=../configuration/development.py \
	  ./run.py"

css : iis/static/css/iis_style.css

js : 
	-mkdir -p ./iis/static/js
	cp components/bootstrap-sass-3.3.7/assets/javascripts/bootstrap.js iis/static/js/


iis/static/css/iis_style.css : iis/static/sass/iis_style.scss
	-mkdir -p ./iis/static/css
	sass --scss -I components/bootstrap-sass-3.3.7/assets/stylesheets/ \
	  iis/static/sass/iis_style.scss:iis/static/css/iis_style.css

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
	rm .installed
