from flask import Blueprint, Response, abort, current_app, request, session
from peewee import IntegrityError

from ..models import OneTimePass
from .func import encrypt_msg, gen_pass, hash_key

admin_routes = Blueprint("admin", __name__, url_prefix="/admin")


@admin_routes.before_request
def before_request():
    config = current_app.config["admin"]

    if not "verified" in session:
        session["verified"] = False
        session["rand_key"] = None

    if not session["verified"]:
        rand_key = gen_pass(32)
        current_app.logger.warning(f"New admin key created: {rand_key}")

        enc_msg = encrypt_msg(rand_key, config["public_key"])
        resp = Response(enc_msg)
        resp.headers["Verification-Status"] = "should_verify"
        session["rand_key"] = rand_key
        session["verified"] = "try"
        return resp

    if session["verified"] == "try":
        if (
            session["rand_key"]
            and "Verification-Status" in request.headers
            and request.headers["Verification-Status"] == "try"
        ):
            if hash_key(session["rand_key"], config["salt"]) == request.data.decode():
                current_app.logger.info("Admin loged in successfuly")
                session["verified"] = True
            else:
                session["verified"] = False
                current_app.logger.warning("Wrong admin reply")
                abort(401)

    if session["verified"] == True:
        current_app.logger.info("verified: True")
        current_app.database.connect()
    else:
        current_app.logger.info("verification try failed")
        abort(403)


@admin_routes.after_request
def after_request(response):
    current_app.database.close()
    return response


@admin_routes.route("/verificate", methods=["POST", "GET"])
def verificate():
    return {"verification": True}


@admin_routes.route("/gen_pass")
def gen_one_time_pass():
    pass_text = gen_pass(64)
    try:
        OneTimePass(password=pass_text).save()
        current_app.logger.warning(f"{request.remote_addr} generated a OneTimePass")
        return {"Success": True, "OneTimePass": pass_text}
    except IntegrityError as e:
        current_app.logger.error(e)
        return {"Success": False, "error": str(e)}
