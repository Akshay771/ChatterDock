import datetime
import traceback

import bcrypt
from app import rtm_app, rtm_app_api, JWT_ACCESS_TOKEN_TIMEDELTA, JWT_REFRESH_TOKEN_TIMEDELTA
from flask import make_response, jsonify, Blueprint, request, Response
from flask_restful import Api, Resource

from app.chats.controller import add_message, get_latest_message_content, retrieve_chats, add_chats, \
    create_chat_session, list_chats
from app.common import success_messages, error_messages
from app.base_response import BaseResponse
from app.common.constants import API_FAILURE_STATUS, API_SUCCESS_STATUS
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
)

from app.celery_config.celery_tasks import user_registration, admin_registration_notification
from app.db_schema.user import Users
from app.master.controller import edit_user, get_user_info
from app.db_schema.message import Message
from app.utils.utilities import generate_unique_string

rtm_app_chat_bp = Blueprint("rtm_app_chat_bp", __name__)


class SendMessage(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.json
            sender = data.get('sender', None)
            receiver = data.get('receiver', None)
            content = data.get('content', None)
            first_message = data.get("first_message", False)
            timestamp = datetime.datetime.utcnow()
            current_user_id = get_jwt_identity()
            print(current_user_id)

            msg_obj = Message()
            msg_obj.sender_id = sender
            msg_obj.receiver_id = receiver
            msg_obj.content = content
            msg_obj.timestamp = timestamp
            msg_obj.first_message = first_message

            msg_id = generate_unique_string()
            # if first_message:
            chat_id = generate_unique_string()
            add_chats(chat_id, msg_id, msg_obj)

            base_resp_obj = BaseResponse()

            if None in [sender, receiver, content, first_message]:
                base_resp_obj.data_message = error_messages.MESSAGE_BODY_INCORRECT
                base_resp_obj.message = API_FAILURE_STATUS
                base_resp_obj.error = error_messages.MESSAGE_BODY_INCORRECT['MSG']
                return base_resp_obj.json()

            add_message(msg_id, msg_obj)
            base_resp_obj.data_message = success_messages.MESSAGE_SENT_SUCCESSFULLY
            base_resp_obj.message = API_SUCCESS_STATUS
            return base_resp_obj.json()

        except Exception as e:
            print("Exception: ", str(e))
            rtm_app.logger.error(traceback.format_exc())
            return error_messages.MESSAGE_NOT_SENT


class RetrieveMessage(Resource):
    @jwt_required()
    def post(self):
        try:
            req_data = request.json
            user_id = req_data.get('user_id', None)
            sender_id = req_data.get('sender_id', None)
            chat_id = req_data.get("chat_id")

            # Retrieve messages based on user_id and sender_id
            msg_content = get_latest_message_content(chat_id)
            print(msg_content)

            return make_response(jsonify({"message": msg_content}))
        except Exception as e:
            # Log the exception
            print("Exception:", str(e))
            rtm_app.logger.error(traceback.format_exc())
            # Return an error response if something goes wrong
            return jsonify({"error": "Internal Server Error"}), 500


class Chats(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.json
            user_id = data.get('user_id', None)
            sender_id = data.get('sender_id', None)

            chats = retrieve_chats(user_id, sender_id)
            return make_response(jsonify({"Chats": chats}))
        except Exception as e:
            # Log the exception
            print("Exception:", str(e))
            rtm_app.logger.error(traceback.format_exc())
            # Return an error response if something goes wrong
            return jsonify({"error": "Internal Server Error"}), 500


class ChatSession(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.json
            started_by = data.get('user_id', None)
            with_user = data.get('recipient_id', None)
            created_at = datetime.datetime.utcnow()
            session_id = generate_unique_string()

            if None in [started_by, with_user]:
                return {"message": "error"}

            create_session = create_chat_session(session_id, started_by, with_user, created_at)
            return make_response(jsonify({"chat_id": create_session}))
        except Exception as e:
            print("Exception:", str(e))
            rtm_app.logger.error(traceback.format_exc())
            # Return an error response if something goes wrong
            return jsonify({"error": "Internal Server Error"}), 500


class ListChats(Resource):
    def post(self):
        try:
            data = request.json
            user_id = data.get("user_name", None)

            if user_id is None:
                return jsonify({"message": "no user id"})
            chat_list = list_chats(user_id)
            print(chat_list)
            if chat_list:
                return make_response(jsonify({"chat_list": chat_list}), 200)
        except Exception as e:
            print("Exception:", str(e))
            rtm_app.logger.error(traceback.format_exc())
            # Return an error response if something goes wrong
            return jsonify({"error": "Internal Server Error"}), 500


rtm_app_api.add_resource(SendMessage, "/api/v1/send-message")
rtm_app_api.add_resource(RetrieveMessage, "/api/v1/ret-message")
rtm_app_api.add_resource(Chats, "/api/v1/chats")
rtm_app_api.add_resource(ChatSession, "/api/v1/chat-session")
rtm_app_api.add_resource(ListChats, "/api/v1/chat-list")
