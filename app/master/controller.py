import copy
import datetime
import time
from app.common import success_messages, error_messages
import bcrypt
from app import mongo, rtm_app
import traceback
import pymongo
import pandas as pd
from app.common.constants import *
from bson.objectid import ObjectId
import os


# def add_user(new_user):
#     try:
#         result = mongo.db.users.insert_one(new_user)
#         return str(result.inserted_id)
#     except pymongo.errors.DuplicateKeyError as e:
#         user_management_app.logger.error(traceback.format_exc())
#         print("Exception: ", str(e))
#         return error_messages.EMAIL_ALREADY_EXISTS
#     except Exception as e:
#         user_management_app.logger.error(traceback.format_exc())
#         print("Exception: ", str(e))
#         return error_messages.REGISTRATION_UNSUCCESSFUL


def edit_user(user_id, user, password):
    try:
        result = None
        # print(user.first_name)

        common_dict = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.full_name,
            'email': user.email,
            'phone': user.phone,
            'password': password,
            'is_password_set': True,
            'is_registered': user.is_registered,
            'date': user.date,
            'edit_date': user.edit_date,
            'first_time_login': user.first_time_login,
            'other_information': None
        }
        print("before mongo update")
        u_email = user.email
        user_exist = mongo.db.users.find_one({"email": f"{u_email}"})

        user_id_exist = mongo.db.users.find_one({"_id": f"{user_id}"})
        print(user_exist, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        if user_exist:
            return error_messages.EMAIL_ALREADY_EXISTS
        elif user_id_exist:
            return error_messages.USER_ID_ALREADY_EXISTS

        else:
            document = {**common_dict, "_id": user_id}
            result = mongo.db.users.insert_one(document)

            print("After mongo update")
            if result.acknowledged == 1:
                return success_messages.REGISTRATION_SUCCESSFUL
            else:
                return error_messages.REGISTRATION_UNSUCCESSFUL

    except Exception as e:
        print("Exception: ", str(e))
        rtm_app.logger.error(traceback.format_exc())
        return error_messages.REGISTRATION_UNSUCCESSFUL


def get_user_info(email, is_registered=False):
    try:
        match = {'email': email}
        if is_registered:
            match.update({'is_registered': True})
        result = mongo.db.users.find_one(match)
        print(result)
        if result is not None:
            return result
        else:
            return error_messages.USER_DOES_NOT_EXIST
    except Exception as e:
        rtm_app.logger.error(traceback.format_exc())
        print("Exception: ", str(e))
        return error_messages.USER_DOES_NOT_EXIST  # In case there is DB Connection Error
