import datetime
import traceback

import bcrypt
from app import rtm_app, rtm_app_api, JWT_ACCESS_TOKEN_TIMEDELTA, JWT_REFRESH_TOKEN_TIMEDELTA
from flask import make_response, jsonify, Blueprint, request, Response
from flask_restful import Api, Resource
from app.common import success_messages, error_messages
from app.base_response import BaseResponse
from app.common.constants import API_FAILURE_STATUS, API_SUCCESS_STATUS, API_ERROR_STATUS
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
)

from app.celery_config.celery_tasks import user_registration, admin_registration_notification
from app.db_schema.user import Users
from app.master.controller import edit_user, get_user_info

rtm_app_master_bp = Blueprint("rtm_app_master_bp", __name__)


class Register(Resource):
    def post(self):
        try:
            user_id = request.json.get("user_id")
            first_name = request.json.get("first_name", None)
            last_name = request.json.get("last_name", None)
            email = request.json.get("email", None)
            phone = request.json.get("phone", None)
            password = request.json.get("password", None)

            base_resp_obj = BaseResponse()

            if None in [user_id, first_name, last_name, email, phone]:
                base_resp_obj.data_message = error_messages.ENTERED_DETAILS_INCORRECT
                base_resp_obj.message = API_FAILURE_STATUS
                base_resp_obj.error = error_messages.ENTERED_DETAILS_INCORRECT['MSG']
                return base_resp_obj.json()

            user = Users()
            user.email = email.lower().strip()
            user.first_name = first_name
            user.last_name = last_name
            user.full_name = user.first_name + " " + user.last_name
            user.phone = phone
            user.is_registered = True
            user.date = datetime.datetime.utcnow()
            user.edit_date = datetime.datetime.utcnow()

            password = password.encode()
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(12))

            result = edit_user(user_id, user, hashed_password)
            print(result)
            full_name = first_name + " " + last_name

            if result == success_messages.REGISTRATION_SUCCESSFUL:
                base_resp_obj.data_message = success_messages.REGISTRATION_SUCCESSFUL
                base_resp_obj.message = API_SUCCESS_STATUS

                # User Registration Email Task
                print("here before submitting celery task")
                user_registration_task = user_registration.delay(email, full_name)
                rtm_app.logger.debug(
                    "User Registration Email Task ID: " + user_registration_task.task_id)

                # Admin Registration Notification Task
                admin_registration_notification_task = admin_registration_notification.delay(first_name, last_name,
                                                                                             email)
                rtm_app.logger.debug(
                    "Admin Registration Notification Email Task ID: " + admin_registration_notification_task.task_id)

            else:
                base_resp_obj.data_message = result
                base_resp_obj.message = API_FAILURE_STATUS
                base_resp_obj.error = result['MSG']
            return base_resp_obj.json()

        except Exception as e:
            rtm_app.logger.error(traceback.format_exc())
            print("Exception: ", str(e))
            base_resp_obj = BaseResponse()
            base_resp_obj.message = API_ERROR_STATUS
            base_resp_obj.code = 500
            base_resp_obj.data_message = error_messages.INTERNAL_SERVER_ERROR
            base_resp_obj.error = error_messages.INTERNAL_SERVER_ERROR['MSG']
            return base_resp_obj.json()


class Login(Resource):
    def post(self):
        try:
            email = request.json.get("email", None)
            password = request.json.get("password", None)

            base_resp_obj = BaseResponse()
            if email is None:
                base_resp_obj.data_message = error_messages.ENTERED_DETAILS_INCORRECT
                base_resp_obj.message = API_FAILURE_STATUS
                base_resp_obj.error = error_messages.ENTERED_DETAILS_INCORRECT['MSG']
                return base_resp_obj.json()

            email = email.lower().strip()
            user_info = get_user_info(email, True)
            if user_info == error_messages.USER_DOES_NOT_EXIST:
                base_resp_obj.data_message = error_messages.USER_DOES_NOT_EXIST
                base_resp_obj.message = API_FAILURE_STATUS
                base_resp_obj.error = error_messages.USER_DOES_NOT_EXIST['MSG']
                return base_resp_obj.json()
            if password is None:
                base_resp_obj.data_message = error_messages.ENTERED_DETAILS_INCORRECT
                base_resp_obj.message = API_FAILURE_STATUS
                base_resp_obj.error = error_messages.ENTERED_DETAILS_INCORRECT['MSG']
                return base_resp_obj.json()

            password_in_db = user_info.get("password")

            entered_password = password.encode()
            if password_in_db is None:
                base_resp_obj.data_message = error_messages.PASSWORD_NOT_SET
                base_resp_obj.message = API_FAILURE_STATUS
                base_resp_obj.error = error_messages.PASSWORD_NOT_SET['MSG']
                return base_resp_obj.json()

            if not bcrypt.checkpw(entered_password, password_in_db):
                base_resp_obj.data_message = error_messages.PASSWORD_INCORRECT
                base_resp_obj.message = API_FAILURE_STATUS
                base_resp_obj.error = error_messages.PASSWORD_INCORRECT['MSG']
                return base_resp_obj.json()

            access_token = create_access_token(identity=email, expires_delta=JWT_ACCESS_TOKEN_TIMEDELTA)
            refresh_token = create_refresh_token(identity=email, expires_delta=JWT_REFRESH_TOKEN_TIMEDELTA)
            tokens = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "email": user_info.get("email"),
            }
            base_resp_obj.data_message = success_messages.AUTHENTICATION_SUCCESSFUL
            base_resp_obj.message = API_SUCCESS_STATUS
            base_resp_obj.result = tokens
            base_resp_obj.user_name = user_info.get("_id")
            return base_resp_obj.json()

        except Exception as e:
            print(str(e))


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        base_response_object = BaseResponse()
        try:
            email = get_jwt_identity()
            user_info = get_user_info(email, True)
            access_token = create_access_token(identity=email, expires_delta=JWT_ACCESS_TOKEN_TIMEDELTA)
            base_response_object.result = {'access_token': access_token}
            base_response_object.data_message = success_messages.AUTHENTICATION_SUCCESSFUL
            base_response_object.message = API_SUCCESS_STATUS
            base_response_object.result = access_token
            return base_response_object.json()
        except Exception as e:
            print("Exception: ", str(e))
            rtm_app.logger.debug(traceback.format_exc())
            base_resp_obj = BaseResponse()
            base_resp_obj.message = API_ERROR_STATUS
            base_resp_obj.code = 500
            base_resp_obj.data_message = error_messages.INTERNAL_SERVER_ERROR
            base_resp_obj.error = error_messages.INTERNAL_SERVER_ERROR['MSG']
            return base_resp_obj.json()


class HealthCheck(Resource):
    def get(self):
        return make_response(jsonify({"health-check": "true"}), 200)


rtm_app_api.add_resource(Register, "/api/v1/user-registration")
rtm_app_api.add_resource(Login, "/api/v1/login")
rtm_app_api.add_resource(HealthCheck, "/api/v1/health-check")
rtm_app_api.add_resource(TokenRefresh, "/api/v1/refresh-token")
