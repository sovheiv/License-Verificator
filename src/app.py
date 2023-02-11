import logging
import logging.config
from peewee import PostgresqlDatabase

import yaml
from flask import Flask

from .config import CustomConfig


def init_logger(app):
    with open("./logger.yaml", "r") as stream:
        loggers_config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(loggers_config)
    app.logger = logging.getLogger(name="verificator")


def init_db(app) -> PostgresqlDatabase:
    app.database = PostgresqlDatabase(**app.config["DB"])


def init_app():
    Flask.config_class = CustomConfig
    app = Flask(__name__)

    app.config.load_config()
    init_logger(app)
    init_db(app)

    app.logger.info("app inited")
    return app
