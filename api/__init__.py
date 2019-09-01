import os, sys
import requests
import time
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_session import Session



from api.api_home import ApiHome
from api.api_metaproxy import ApiMetaProxy

api = Api()
session = Session()
cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.config')
    
    api.add_resource(ApiHome, '/')
    api.add_resource(ApiMetaProxy, '/metaproxy')

    api.init_app(app)
    cors.init_app(app)

    return app


