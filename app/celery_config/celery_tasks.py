import base64
import copy
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pytz
from celery.schedules import crontab
from dateutil import parser
from app import rtm_app, mail
from flask_mail import Message
from app import celery_app, mongo
import traceback
import os

print("in celery task")


@celery_app.task(name='user_registration')
def user_registration(email, full_name):
    try:
        print("in reg celery task")
        email_body_content = (
            f"<p>Hi {full_name},</p>"
            "<p>Thank you for registering with RTM Messaging. We're glad to have you on board!</p>"
            "<p>With RTM Messaging, you can stay connected with friends, family, and colleagues, share important updates, and collaborate seamlessly.</p>"
            "<p>Feel free to explore our features and reach out to us if you have any questions or feedback.</p>"
            "<p>Happy messaging!</p>"
            "<br>"
            "<p>Best regards,</p>"
            "<p>RTM Messaging Team</p>"
        )

        print(f"EMAIL BODY CONTENT:\n {email_body_content}")

        # subject = 'Thank you for registering'
        subject = "Welcome to RTM Messaging!"
        sender_id = rtm_app.config['MAIL_USERNAME']
        sender_name = rtm_app.config['SENDER_NAME']
        sender_data = (sender_name, sender_id)
        msg = Message(
            subject,
            sender=sender_data,
            recipients=[email]
        )

        with rtm_app.app_context():
            msg.html = email_body_content
            mail.send(msg)

    except Exception as e:
        rtm_app.logger.error(traceback.format_exc())
        print("Exception: ", str(e))


@celery_app.task(name='admin_registration_notification')
def admin_registration_notification(first_name, last_name, user_email):
    try:
        # link to see registered user work on this after user reg and admin notification !!!!!!!!!!!!!!!!!!!!!!!!
        # admin_portal_url = os.environ.get("VUE_BASE_URL")  # send url to see admin reg users
        reg_date = datetime.datetime.now()
        admin_email = "rathodakshay902@gmail.com"
        email_body_content = (
            "<p>Hi Admin,</p>"
            "<p>A new user has registered with RTM Messaging. Here are the details:</p>"
            f"<p>Name: {first_name} {last_name}</p>"
            f"<p>Email: {user_email}</p>"
            f"<p>Registration Date: {reg_date}</p>"
            "<p>As an admin, you can review the new user's information and take any necessary actions.</p>"
            "<p>If you have any questions or concerns, feel free to reach out to us.</p>"
            "<br>"
            "<p>Best regards,</p>"
            "<p>RTM Messaging Team</p>"
        )

        subject = "RTM Messaging Admin Notification: New User Registration"
        sender_id = rtm_app.config['MAIL_USERNAME']
        sender_name = rtm_app.config['SENDER_NAME']
        sender_data = (sender_name, sender_id)
        msg = Message(
            subject,
            sender=sender_data,
            recipients=[admin_email]
        )

        with rtm_app.app_context():
            msg.html = email_body_content
            mail.send(msg)

    except Exception as e:
        rtm_app.logger.error(traceback.format_exc())
        print("Exception: ", str(e))
