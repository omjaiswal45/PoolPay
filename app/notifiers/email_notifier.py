from app.notifiers.base_notifier import BaseNotifier
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


class EmailNotifier(BaseNotifier):

    def send(self, recipient: str, message: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = "noreply@poolpay.com"
            msg['To'] = recipient
            msg['Subject'] = "PoolPay Notification"
            msg.attach(MIMEText(message, 'plain'))
            return True
        except Exception:
            return False