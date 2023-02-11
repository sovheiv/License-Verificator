import random
import string
from datetime import timedelta

from environs import Env
from flask import Config

env = Env()
env.read_env(override=True)


class CustomConfig(Config):
    def load_config(self):
        with env.prefixed("DB_"):
            self["DB"] = {
                "database": env.str("NAME"),
                "host": env.str("HOST"),
                "port": env.int("PORT"),
                "user": env.str("USER"),
                "password": env.str("PASSWORD"),
            }
        with env.prefixed("ADMIN_"):
            self["admin"] = {
                "public_key": env.str("PUBLIC_KEY"),
                "salt": env.str("SALT"),
            }
        with env.prefixed("USER_"):
            self["user"] = {
                "key_salt": env.str("KEY_SALT"),
                "msg_salt": env.str("MSG_SALT"),
            }

        with env.prefixed("FLASK_"):
            self["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=env.int("PERMANENT_SESSION_LIFETIME"))
            self["SECRET_KEY"] = self.gen_pass(env.int("SECRET_KEY_LEN"))

    @staticmethod
    def gen_pass(size=32, chars=string.ascii_lowercase + string.digits):
        return "".join(random.choice(chars) for _ in range(size))
