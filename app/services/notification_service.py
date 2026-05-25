from app.notifiers.base_notifier import BaseNotifier


class NotificationService:

    def __init__(self, notifier: BaseNotifier):
        self.notifier = notifier

    def notify_low_balance(self, members: list, pool_name: str):
        for member in members:
            self.notifier.send(
                member.get('email') or member.get('phone'),
                f"PoolPay Alert: '{pool_name}' balance is running low. Please top up soon."
            )

    def notify_transaction(self, members: list, user_name: str, amount: str, type: str, pool_name: str):
        action = "spent" if type == "expense" else "added"
        for member in members:
            self.notifier.send(
                member.get('email') or member.get('phone'),
                f"PoolPay: {user_name} {action} ₹{amount} in '{pool_name}'"
            )

    def notify_member_joined(self, admin_email: str, member_name: str, pool_name: str):
        self.notifier.send(
            admin_email,
            f"PoolPay: {member_name} has joined your pool '{pool_name}'"
        )

    def notify_invite_sent(self, phone: str, pool_name: str, token: str):
        self.notifier.send(
            phone,
            f"PoolPay: You have been invited to join '{pool_name}'. Click here to join: https://poolpay.com/invite/{token}"
        )

    def notify_member_added(self, email: str, pool_name: str):
        self.notifier.send(
            email,
            f"PoolPay: You have been added to pool '{pool_name}'"
        )

    def notify_member_removed(self, email: str, pool_name: str):
        self.notifier.send(
            email,
            f"PoolPay: You have been removed from pool '{pool_name}'"
        )