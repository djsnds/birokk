from celery import Celery
from settings import RABBITMQ_URL
from settings import DATABASE_URL
from pytz import timezone


celery_app = Celery(
    "celery_app",
    broker=RABBITMQ_URL,
    include="celery_app.celery_tasks",
)


celery_app.conf.update(
    beat_dburi=DATABASE_URL,
    beat_scheduler="celery_sqlalchemy_scheduler.schedulers:DatabaseScheduler",
    beat_max_loop_interval=5,
    timezone=timezone("UTC"),
    task_queues={
        "notifications": {
            "exchange": "celery",
            "exchange_type": "direct",
            "routing_key": "notifications"
        },
        "information": {
            "exchange": "celery",
            "exchange_type": "direct",
            "routing_key": "information"
        },
        "results": {
            "exchange": "celery",
            "exchange_type": "direct",
            "routing_key": "results"
        },
    },
    task_routes={
        "send_notification": {"queue": "notifications"},
        "send_information": {"queue": "information"},
        "send_admission_list": {"queue": "results"},
    }
)

