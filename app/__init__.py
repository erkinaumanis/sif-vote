# this code allows us to import modules inside the lib directory
import sys, os 
sys.path.insert(0, os.path.abspath(".."))

from flask import Flask

# init
app = Flask(__name__)

def config_str_to_obj(cfg):
    if isinstance(cfg, basestring):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg

def start_app(config):
    app = Flask(__name__)

    config = config_str_to_obj(config)
    configure_app(app,config)
    configure_database(app)
    configure_blueprints(app)

    return app

def configure_app(app,config):
    app.config.from_object(config)
    app.config.from_envvar("APP_CONFIG", silent=True)
    app.config['SERVER_NAME'] = '0.0.0.0:5000'

def configure_blueprints(app):
    from views import views
    app.register_blueprint(views)

def configure_database(app):
    from database import Database
    Database(app=app)