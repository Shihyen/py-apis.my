import os
import redis
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    LOG_PATH = '/app/logs'
    DEBUG = True
    TESTING = True
    APPLICATION_NAME = "MyAPI"

    CORS_HEADERS = 'Content-Type'
    CORS_RESOURCES = {r"/api/*": {"origins": "*"}}
    CORS_METHODS = ['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'HEAD']

    SECRET_KEY = "How are you, I'm fine, thank you!"
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = True
    SESSION_USE_SINGER = True
    SESSION_KEY_PREFIX = "metaproxy_session:"
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379', password='')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

configs = {
    'development': DevelopmentConfig
}