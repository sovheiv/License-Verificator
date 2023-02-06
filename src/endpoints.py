import hashlib
import json

from flask import Blueprint, current_app, request
import os

admin = Blueprint("admin", __name__)


@admin.route("/")
def index():
    current_app.logger.info("test")
    return {"page": "Main page", "env_var_test": os.getenv("TEST_ENV_NUM")}


@admin.route("/verificate", methods=["POST"])
def verificate():
    webhook = json.loads(request.data.decode())
    current_app.logger.info("Verification start")

    current_app.logger.debug(webhook)

    hashed = hash_key(os.getenv("KEY1") + webhook["key2"])

    if hashed == webhook["key1"]:
        resp = hash_key(os.getenv("KEY2") + webhook["key2"])
        current_app.logger.info("Verification completed")
        return {"success": resp}

    current_app.logger.info("Verification faild")
    return {"success": False}


def hash_key(key):
    return hashlib.sha512(str.encode(key + "kaban")).hexdigest()


@admin.app_errorhandler(404)
def handle_404(error):
    print(error)
    return "<center><b> Page not found </b></center>"
