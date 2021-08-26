from lib.ms_teams import send_alert
from api.event import subscribe


def handle_send_teams_alert(who, alert_template):
    send_alert(f"{who}: {alert_template}")


def setup_alert_event_handlers():
    subscribe("send_teams_alert", handle_send_teams_alert)
