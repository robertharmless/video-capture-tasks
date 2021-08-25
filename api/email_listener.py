from lib.email import send_email
from api.event import subscribe


def handle_send_email(who, generated_template):
    send_email(f"{who}: {generated_template}")


def setup_email_event_handlers():
    subscribe("send_email", handle_send_email)
