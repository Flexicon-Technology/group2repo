from flask import Flask, request
from flask_restx import Resource, Api, Namespace, fields
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

server = Flask(__name__)
api = Api(server)

# Namespace to organize endpoints in the API
authentication_namespace = Namespace('auth', description='A namespace for authentication')

# Defining registration fields/models
register_model = authentication_namespace.model(
    'Register', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="Username"),
        'email': fields.String(required=True, description='Email'),
        'password': fields.String(required=True, description='Password')
    }
)

# Defining user fields/models
user_model = authentication_namespace.model(
    'User', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="Username"),
        'email': fields.String(required=True, description='Email'),
        'password_hash': fields.String(required=True, description='Password')
    }
)

# Defining login fields/models
login_model = authentication_namespace.model(
    'Login', {
        'email': fields.String(required=True, description='Email'),
        'password': fields.String(required=True, description='Password')
    }
)

# Register class
@authentication_namespace.route('/register', methods=["POST"])
class Register(Resource):
    
    # Register Function/create user
    #@register_model.expect(register_model)
    @authentication_namespace.marshal_with(user_model)
    def post(self):

        data = request.get_json()

        new_user = User(
            username = data.get('username'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password'))
        )

        new_user.save()
        return new_user, HTTPStatus.CREATED
    
# Login class
@authentication_namespace.route('/login')
class Login(Resource):

    # Login Function 
    @authentication_namespace.expect(login_model)
    def post(self):

        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if (user is not None) & check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.OK
        
# Refresh class
@authentication_namespace.route('/refresh')
class Refresh(Resource):

    # function to generate new jwt access token incase tokens expires/page refresh
    @jwt_required(refresh=True)
    def post(self):
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {"access_token": access_token}, HTTPStatus.OK


