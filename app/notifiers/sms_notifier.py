from app.notifiers.base_notifier import BaseNotifier


class SMSNotifier(BaseNotifier):
    async def send(self, recipient: str, subject: str, body: str) -> None:
        raise NotImplementedError
