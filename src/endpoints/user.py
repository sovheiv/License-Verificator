from datetime import datetime

from flask import Blueprint, abort, current_app, request
from peewee import DoesNotExist, IntegrityError

from ..models import ApiKey, OneTimePass, UserTb
from .func import gen_rsa_keys

user_routes = Blueprint("user", __name__)


@user_routes.before_request
def before_request():
    current_app.database.connect()


@user_routes.after_request
def after_request(response):
    current_app.database.close()
    return response


@user_routes.route("/create_key")
def create_key():
    curr_ip = request.remote_addr
    user_ot_pass = request.args.get("otpass")
    name = request.args.get("name")
    password = request.args.get("pass")

    try:
        one_time_pass = OneTimePass.get(OneTimePass.password == user_ot_pass)
    except DoesNotExist:
        current_app.logger.info(f"{curr_ip} tried to create key with wrong pass")
        abort(403)

    if one_time_pass.expiration_time < datetime.now():
        current_app.logger.info(f"{curr_ip} tried to create key with expierd pass")
        abort(403)
    if one_time_pass.is_activated:
        current_app.logger.info(f"{curr_ip} tried to create key with used pass")
        abort(403)

    with current_app.database.atomic() as transaction:
        try:
            user = get_user(name, password, curr_ip)

            public_key, private_key = gen_rsa_keys()
            apikey = ApiKey.create(public_key=public_key, private_key=private_key, fk_user=user)

            one_time_pass.activation_time = datetime.now()
            one_time_pass.activation_ip = curr_ip
            one_time_pass.is_activated = True
            one_time_pass.generated_user = user
            one_time_pass.generated_key = apikey
            one_time_pass.save()

        except IntegrityError as error:
            transaction.rollback()
            print(error)
            current_app.logger.info(f"{curr_ip} creation failed: {error}")
            return {"success": False, "msg": str(error)}

    current_app.logger.info(f"{curr_ip} created ApiKey")
    return {"success": True, "msg": f"User: {name} created for ip: {curr_ip}. Key added."}


def get_user(name, password, curr_ip):
    try:
        user = UserTb.get(UserTb.name == name)
        if user.password != password:
            current_app.logger.info(f"{curr_ip} wrong password. User: {name}")
            abort(403)
        if curr_ip not in user.ip:
            current_app.logger.info(f"{curr_ip} wrong ip. User: {name}")
            abort(403)

    except DoesNotExist:
        user = UserTb.create(name=name, password=password, ip=[curr_ip])
        current_app.logger.info(f"New user created: {name}")

    return user
