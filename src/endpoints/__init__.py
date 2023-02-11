from .user import user_routes
from .admin import admin_routes
from .common import common_routes


all_routes = [user_routes, admin_routes, common_routes]
