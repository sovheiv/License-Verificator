from flask import Blueprint

common_routes = Blueprint("common", __name__)


@common_routes.route("/favicon.ico")
def favicon():
    return {"favicon": False}


@common_routes.app_errorhandler(404)
def handle_404(error):
    print(error)
    return "<center><b> Page not found </b></center>"
