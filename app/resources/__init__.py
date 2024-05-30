from flask import Blueprint
from flask_restful import Api
from .user import UserResource
from .order import OrderResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(UserResource, '/users')
api.add_resource(OrderResource, '/orders')
