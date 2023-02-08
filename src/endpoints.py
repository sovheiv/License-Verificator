import hashlib
import os

import rsa
from flask import Blueprint, current_app, request

admin = Blueprint("admin", __name__)


@admin.route("/")
def index():
    current_app.logger.info("Main page")
    return {"page": "Main page", "env_var_test": os.getenv("TEST_ENV_NUM")}

@admin.route("/verificate", methods=["POST"])
def verificate():
    key_hash = request.headers["Authorization"]
    enc_msg = request.data
    
    current_app.logger.info(f"Verification started for {request.remote_addr}")

    if hash_key(os.getenv("PUBLIC_KEY"), os.getenv("IN_SALT")) != key_hash:
        current_app.logger.info("Key not found by hash")
        return {"success": False}

    current_app.logger.info("Key exist")

    privat_key = rsa.PrivateKey.load_pkcs1(os.getenv("PRIVAT_KEY"))
    dec_msg = rsa.decrypt(enc_msg, privat_key).decode()

    return {"success": hash_key(dec_msg, os.getenv("OUT_SALT"))}


def hash_key(key, salt):
    return hashlib.sha256(str.encode(key + salt)).hexdigest()


@admin.app_errorhandler(404)
def handle_404(error):
    print(error)
    return "<center><b> Page not found </b></center>"
