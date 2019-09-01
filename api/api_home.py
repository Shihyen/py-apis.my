from flask_restful import Resource
from flask import current_app

class ApiHome(Resource):
    def get(self):
        # current_app.logger.info('API Home')
        print("hi")
        return "API home"