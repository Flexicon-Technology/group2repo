from flask_restful import Resource

class OrderResource(Resource):
    def get(self):
        return {'message': 'List of orders'}

    def post(self):
        return {'message': 'Order created'}
