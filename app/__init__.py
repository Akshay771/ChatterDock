import datetime
from functools import wraps

from app.base_response import BaseResponse
from app.common import error_messages
from app.common.constants import *
from dotenv import load_dotenv
from flask import Flask, make_response, jsonify, request
from flask_restful import Api
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_mail import Mail
import os
from app.celery_config.celery_worker import make_celery
from flask_jwt_extended import JWTManager, verify_jwt_in_request

# creates a Flask application instance named rtm_app
rtm_app = Flask(__name__)
# Cross-Origin Resource Sharing (CORS) for a Flask application (rtm_app), allowing all resources to be accessed from
# any origin
# cors = CORS(rtm_app, resources={r'*': {"origins": '*'}})
cors = CORS(rtm_app, resources={r'*': {"origins": ['*']}})
print(os.environ.get('MONGO_URI'))
# rtm_app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
# rtm_app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
# rtm_app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
# rtm_app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
# rtm_app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
# rtm_app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# rtm_app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# rtm_app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER')
# rtm_app.config['BROKER_URL'] = os.environ.get('CELERY_BROKER')
# rtm_app.config["ADMIN_EMAIL"] = os.environ.get("ADMIN_EMAIL")

rtm_app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/RTM"
rtm_app.config['MAIL_SERVER'] = "smtp.gmail.com"
rtm_app.config['MAIL_PORT'] = 587
rtm_app.config['MAIL_USE_TLS'] = True
rtm_app.config['MAIL_USE_SSL'] = False
rtm_app.config['MAIL_USERNAME'] = "rathodakshay293@gmail.com"
rtm_app.config['MAIL_PASSWORD'] = "jbiqtvazclmvjtsn"
rtm_app.config['CELERY_BROKER_URL'] = "amqp://127.0.0.1:5672"
rtm_app.config['BROKER_URL'] = "amqp://127.0.0.1:5672"
rtm_app.config["ADMIN_EMAIL"] = "rathodakshay902@gmail.com"
rtm_app.config['SENDER_NAME'] = "rathodakshay293@gmail.com"

# JWT
rtm_app.config['JWT_SECRET_KEY'] = "0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a"
rtm_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 15 * 60))
rtm_app.config['JWT_REFRESH_TOKEN_EXPIRES'] = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 24 * 60 * 60))
rtm_app.config['JWT_BLACKLIST_ENABLED'] = True
rtm_app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
rtm_app.config['PROPAGATE_EXCEPTIONS'] = True

print(rtm_app.config['MONGO_URI'])
mongo = PyMongo(rtm_app)
mail = Mail(rtm_app)
celery_app = make_celery(rtm_app)
rtm_app_api = Api(rtm_app)

rtm_app_jwt = JWTManager(rtm_app)
rtm_app_jwt.init_app(rtm_app)

JWT_ACCESS_TOKEN_TIMEDELTA = datetime.timedelta(minutes=15)
JWT_REFRESH_TOKEN_TIMEDELTA = datetime.timedelta(hours=24)
