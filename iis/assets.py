from flask_assets import Bundle
from webassets.filter import get_filter
from webassets_browserify import Browserify

static_js = Bundle(
    'bower_components/jquery/dist/jquery.js',
    'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
    output='gen/static_js.js'
)

scss_filter = get_filter(
    'scss',
    load_paths=['bower_components/bootstrap-sass/assets/stylesheets/']
)
scss = Bundle(
    'sass/iis_style.scss',
    filters=scss_filter,
    output='gen/iis_style.css'
)

graph_js = Bundle(
    'js/graph.js',
    filters=Browserify,
    output='gen/graph.js'
)
