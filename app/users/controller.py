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


def find_user(recipient_id):
    try:
        result = mongo.db.users.find_one({"_id": recipient_id})
        if result is not None:
            return success_messages.USER_FOUND
        else:
            return error_messages.NO_USER_FOUND

    except Exception as e:
        print("Exception: ", str(e))
        rtm_app.logger.error(traceback.format_exc())
        return error_messages.NO_USER_FOUND
