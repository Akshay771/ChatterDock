import datetime

from app.db_schema.message import Message


def send_message(message, message_id, sender_id,  receiver_id):
    msg = Message()
    msg.sender_id = sender_id
    msg.receiver_id = receiver_id
    msg.message_id = message_id
    msg.content = message
    msg.timestamp = datetime.datetime.utcnow()
