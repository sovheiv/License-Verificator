
import logging
import logging.config

import yaml
from flask import Config, Flask
from endpoints import admin

class YamlConfig(Config):
    def from_yaml(self, config_file="config.yaml"):
        with open(config_file, "r") as stream:
            config = yaml.load(stream, Loader=yaml.FullLoader)
        for key, val in config.items():
            self[key] = val


with open("./logger.yaml", "r") as stream:
    loggers_config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(loggers_config)
logger = logging.getLogger(name="verificator")

def create_app():
    Flask.config_class = YamlConfig
    app = Flask(__name__)
    app.register_blueprint(admin)
    app.config.from_yaml()
    app.logger = logger    
    print("app created")
    return app


app = create_app()