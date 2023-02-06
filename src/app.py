import logging
import logging.config

import yaml
from flask import Config, Flask
from environs import Env

from .endpoints import admin


with open("./logger.yaml", "r") as stream:
    loggers_config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(loggers_config)
logger = logging.getLogger(name="verificator")


def create_app():
    app = Flask(__name__)
    app.register_blueprint(admin)

    env = Env()
    env.read_env(override=True)
    app.config.from_prefixed_env()

    print(app.config)
    app.logger = logger
    print("app created")
    return app
