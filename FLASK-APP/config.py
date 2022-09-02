
import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os .environ.get('DATABASE_URL') or 'postgresql://postgres:sumaiya12@localhost:5432/flask_project'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = os.getenv('REDIS_SERVER','localhost')
    CACHE_REDIS_URL = "redis://"+CACHE_REDIS_HOST+":6379/0"
    CACHE_DEFAULT_TIMEOUT = 3300