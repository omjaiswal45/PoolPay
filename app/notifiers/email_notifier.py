from app.notifiers.base_notifier import BaseNotifier


class EmailNotifier(BaseNotifier):
    async def send(self, recipient: str, subject: str, body: str) -> None:
        raise NotImplementedError
