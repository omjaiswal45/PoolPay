from app.notifiers.base_notifier import BaseNotifier
from app.core.config import settings


class SMSNotifier(BaseNotifier):

    def send(self, recipient: str, message: str) -> bool:
        try:
            from twilio.rest import Client
            client = Client(
                settings.TWILIO_SID,
                settings.TWILIO_AUTH_TOKEN
            )
            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE,
                to=recipient
            )
            return True
        except Exception:
            return False