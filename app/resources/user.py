from flask_restful import Resource

class UserResource(Resource):
    def get(self):
        return {'message': 'List of users'}

    def post(self):
        return {'message': 'User created'}
