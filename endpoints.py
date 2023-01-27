import json
import hashlib

from flask import Blueprint, current_app, request

admin = Blueprint("admin", __name__)


@admin.route("/")
def index():
    return {"verificator": True}
    


@admin.route("/verificate", methods=["POST"])
def verificate():
    webhook = json.loads(request.data.decode())
    current_app.logger.info("Verification start")

    current_app.logger.debug(webhook)

    hashed = hash_key(current_app.config["startup_api_key"] + webhook["key2"])
    

    if hashed == webhook["key1"]:
        resp = hash_key(current_app.config["startup_server_key"] + webhook["key2"])
        current_app.logger.info("Verification completed")
        return{"success": resp}

    current_app.logger.info("Verification faild")
    return{"success": False}

def hash_key(key):
    return hashlib.sha512(str.encode(key+"kaban")).hexdigest()

@admin.app_errorhandler(404)
def handle_404(error):
    print(error)
    return "<center><b><mark> Page not found </mark></b></center>"
