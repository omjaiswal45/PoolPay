from celery import Celery
from app.core.config import settings

celery_app = Celery("poolpay", broker=settings.CELERY_BROKER_URL)


@celery_app.task
def send_notification_task(recipient: str, subject: str, body: str):
    pass
