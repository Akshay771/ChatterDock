import os
from celery import Celery

print("here in celery worker")

# Define Celery app outside make_celery()
celery_app = Celery(
    'RTM_app',
    broker='amqp://127.0.0.1:5672',  # RabbitMQ (default guest:guest)
    backend=None,
    include=['app.celery_config.celery_tasks']
)

def make_celery(app):
    print("RabbitMQ URI:", app.config['CELERY_BROKER_URL'])
    celery_app.conf.update(app.config)
    return celery_app