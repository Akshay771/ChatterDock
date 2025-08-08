import json
import traceback
from app.common import success_messages, error_messages
from app import mongo, rtm_app
from app.common.constants import *
from app.utils.utilities import generate_unique_string


def add_message(msg_id, msg_obj):
    try:
        message_body = {
            'sender_id': msg_obj.sender_id,
            'receiver_id': msg_obj.receiver_id,
            'msg_content': msg_obj.content,
            'time_stamp': msg_obj.timestamp,
            "first_message": msg_obj.first_message
        }

        document = {**message_body, "_id": msg_id}
        result = mongo.db.message.insert_one(document)

        if result.acknowledged == 1:
            return success_messages.MESSAGE_ADDED_SUCCESSFULLY
        else:
            return error_messages.MESSAGE_NOT_ADDED

    except Exception as e:
        rtm_app.logger.error(traceback.format_exc())
        return error_messages.MESSAGE_NOT_ADDED


# def get_latest_message_content(chat_id):
#     try:
#         chat = mongo.db.chats.find_one({'_id': chat_id})
#
#         latest_message_id = chat.get('chat_data', {}).get('messages', [])[-1].get('message_id')
#
#         latest_message = mongo.db.message.find_one({'_id': latest_message_id})
#
#         message_content = latest_message.get('msg_content',
#                                              'Message not found') if latest_message else 'Message not found'
#         return message_content
#
#     except Exception as e:
#         rtm_app.logger.error(traceback.format_exc())
#         return None

def get_latest_message_content(chat_id):
    try:
        chat = mongo.db.chats.find_one({'_id': chat_id})
        messages = chat.get('chat_data', {}).get('messages', [])

        if not messages:
            return 'No messages yet'

        latest_message_id = messages[-1].get('message_id')
        latest_message = mongo.db.message.find_one({'_id': latest_message_id})

        message_content = latest_message.get('msg_content', 'Message not found') if latest_message else 'Message not found'
        return message_content

    except Exception as e:
        rtm_app.logger.error(traceback.format_exc())
        return None


def retrieve_chats(user_id, sender_id):
    try:
        chats = list(mongo.db.message.find(
            {"$or": [{"sender_id": sender_id, "receiver_id": user_id},
                     {"sender_id": user_id, "receiver_id": sender_id}]}))
        return chats
    except Exception as e:
        rtm_app.logger.error(traceback.format_exc())
        return None


def add_chats(chat_id, message_id, msg_obj):
    try:
        # here if there is no chat id exist it will create chat id but it checks the same first
        existing_chat = mongo.db.chats.find_one({
            '$or': [
                {'chat_data.sender_id': msg_obj.sender_id, 'chat_data.receiver_id': msg_obj.receiver_id},
                {'chat_data.sender_id': msg_obj.receiver_id, 'chat_data.receiver_id': msg_obj.sender_id}
            ]
        })

        if existing_chat:
            mongo.db.chats.update_one(
                {'_id': existing_chat['_id']},
                {'$push': {'chat_data.messages': {'message_id': message_id}}}
            )
        else:
            chat_obj = {
                'sender_id': msg_obj.sender_id,
                'receiver_id': msg_obj.receiver_id,
                'messages': [{'message_id': message_id}]
            }
            mongo.db.chats.insert_one({'_id': chat_id, 'chat_data': chat_obj})
    except Exception as e:
        rtm_app.logger.error(traceback.format_exc())


def create_chat_session(session_id, started_by, with_user, created_at):
    try:
        sender_exists = mongo.db.users.find_one({"_id": started_by})
        receiver_exists = mongo.db.users.find_one({"_id": with_user})

        if not sender_exists or not receiver_exists:
            return {"message": "One or both users do not exist", "session_id": None}

        chat_document = mongo.db.chats.find_one({
            "$or": [
                {"chat_data.sender_id": started_by, "chat_data.receiver_id": with_user},
                {"chat_data.sender_id": with_user, "chat_data.receiver_id": started_by}
            ]
        })
        print(chat_document)
        if chat_document:
            chat_id = chat_document["_id"]
            print("1")
            existing_session = mongo.db.chatsession.find_one({
                "$or": [
                    {"started_by": started_by, "with_user": with_user},
                    {"started_by": with_user, "with_user": started_by}
                ]
            })

            if existing_session:
                mongo.db.chatsession.update_one(
                    {"_id": existing_session["_id"]},
                    {"$set": {"chat_id": chat_id}}
                )
                return {"message": "Chat session already exists", "session_id": existing_session["_id"],
                        "chat_id": chat_id}
            else:
                print("here else")
                mongo.db.chatsession.insert_one(
                    {"_id": session_id, "started_by": started_by, "with_user": with_user, "created_at": created_at,
                     "chat_id": chat_id})
                return {"message": "chat session created", "session_id": session_id,
                        "chat_id": chat_id}

        else:
            print("5")
            new_chat_id = generate_unique_string()
            chat_data = {
                "sender_id": started_by,
                "receiver_id": with_user,
                "messages": [
                ]
            }
            mongo.db.chats.insert_one({"_id": new_chat_id, "chat_data": chat_data})
            print("here before chatseesion")
            mongo.db.chatsession.insert_one(
                {"_id": session_id, "started_by": started_by, "with_user": with_user, "created_at": created_at, "chat_id": new_chat_id})
            return {"message": "Chat session created successfully", "session_id": session_id}
    except Exception as e:
        rtm_app.logger.error(traceback.format_exc())
        return {"message": "Error creating chat session", "session_id": None}


def list_chats(user_id):
    try:
        chats = mongo.db.chatsession.find({
            '$or': [
                {'started_by': user_id},
                {'with_user': user_id}
            ]
        })

        # Convert the cursor to a list of dictionaries
        chats_list = list(chats)

        chat_with = []

        for chat in chats_list:
            if chat['started_by'] != user_id:
                chat_with.append({"user": chat['started_by'], "chat_id": chat['chat_id']})
            elif chat['with_user'] != user_id:
                chat_with.append({"user": chat['with_user'], "chat_id": chat['chat_id']})

        # Construct JSON object
        response = {
            "chat_with": chat_with
        }

        return response
    except Exception as e:
        rtm_app.logger.error(traceback.format_exc())
        return {"message": "Error retrieving chat sessions", "session_id": None}



