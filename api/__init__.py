from flask import Flask
import os

import sys
import logging
sys.path.append('../src')
from src.network_trainer import train
net = train()

def create_log(app):
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

def create_app():
    from api.instance.config import Config
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import upload
    app.register_blueprint(upload.bp)

    create_log(app)

    return app


