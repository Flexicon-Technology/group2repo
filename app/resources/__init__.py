from flask import Blueprint
from flask_restful import Api

from user_authapi import Login, Refresh, Register
from .user import UserResource
from .order import OrderResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(UserResource, '/users')
api.add_resource(OrderResource, '/orders')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Refresh, '/refresh')
