import datetime
import traceback

import bcrypt
from app import rtm_app, rtm_app_api, JWT_ACCESS_TOKEN_TIMEDELTA, JWT_REFRESH_TOKEN_TIMEDELTA
from flask import make_response, jsonify, Blueprint, request, Response
from flask_restful import Api, Resource
from app.common import success_messages, error_messages
from app.base_response import BaseResponse
from app.common.constants import API_FAILURE_STATUS, API_SUCCESS_STATUS, API_ERROR_STATUS, \
    PENDING_STATUS, APPROVED_STATUS, REJECTED_STATUS, DISABLED_STATUS, \
    DEACTIVATED_STATUS
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
)

from app.celery_config.celery_tasks import user_registration, admin_registration_notification
from app.db_schema.user import Users
from app.master.controller import edit_user, get_user_info
from app.users.controller import find_user

rtm_app_user_bp = Blueprint("rtm_app_user_bp", __name__)


class SearchUser(Resource):
    def post(self):
        try:
            data = request.json
            recipient_id = data.get("recipient_id", None)
            print(recipient_id)
            base_resp_obj = BaseResponse()
            if recipient_id is None:
                base_resp_obj.data_message = error_messages.NO_USER_FOUND
                base_resp_obj.message = API_FAILURE_STATUS
                base_resp_obj.error = error_messages.NO_USER_FOUND['MSG']
                return base_resp_obj.json()
            user_result = find_user(recipient_id)
            if user_result == success_messages.USER_FOUND:
                base_resp_obj.data_message = success_messages.USER_FOUND
                base_resp_obj.message = API_SUCCESS_STATUS
                base_resp_obj.user_name = recipient_id
                print(base_resp_obj.user_name)

            else:
                base_resp_obj.data_message = user_result
                base_resp_obj.message = API_FAILURE_STATUS
                base_resp_obj.error = user_result['MSG']
            print(base_resp_obj.json())
            return base_resp_obj.json()

        except Exception as e:
            rtm_app.logger.error(traceback.format_exc())
            print("Exception: ", str(e))
            base_resp_obj = BaseResponse()
            base_resp_obj.message = API_ERROR_STATUS
            base_resp_obj.code = 500
            base_resp_obj.data_message = error_messages.INTERNAL_SERVER_ERROR
            base_resp_obj.error = error_messages.INTERNAL_SERVER_ERROR['MSG']
            print(base_resp_obj.json())
            return base_resp_obj.json()


rtm_app_api.add_resource(SearchUser, "/api/v1/search-user")
