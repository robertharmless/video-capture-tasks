"""
Email Processes
"""
# Built-in

# Special
import requests

# App
from .metadata import Metadata
from api.event import post_event
from .config import App

app = App()


class VideoAlert:
    """
    Default Settings to send a Video Alert API Call.
    """

    url = None
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    body = None
    timeout = 120  # seconds
    result = None
    success = False

    # body content
    alertSourceName = app.appname
    alertSourceIP = app.hostname
    alertMessage = ""
    level = "DEBUG"
    sendText = False
    sendEmail = False
    sendTeamsChat = True

    def __init__(
        self,
        alertMessage="",
        level="DEBUG",
        sendText=False,
        sendEmail=False,
        sendTeamsChat=True,
    ):

        self.alertMessage = alertMessage
        self.level = level
        self.sendText = sendText
        self.sendEmail = sendEmail
        self.sendTeamsChat = sendTeamsChat
        self.url = app.video_alert_url

    def set_body(self):
        # prepare the body content.
        data = {
            "alertSourceName": self.alertSourceName,
            "alertSourceIP": self.alertSourceIP,
            "alertMessage": self.alertMessage,
            "level": self.level,
            "sendText": self.sendText,
            "sendEmail": self.sendEmail,
            "sendTeamsChat": self.sendTeamsChat,
        }
        self.body = data

    def send_alert(self):
        """
        Make api call based on the data parameters.
        """
        func = f"{__class__.__name__}.send_alert"

        result = False
        post_event("log_info", f"{func}", f"Starting Api Call to {self.url}")

        response = requests.post(url=self.url, headers=self.headers, json=self.body)
        post_event(
            "log_debug", f"{func}", f"Api Call Status Code:{response.status_code}"
        )

        if response.raise_for_status():
            post_event("log_exception", f"{func}", f"{response.raise_for_status()}")

        if response.ok:
            self.result = response.text
            post_event("log_debug", f"{func}", f"Api Call Result:{response.text}")
            result = True

        return result


def send_alert(who: str, alert_template: dict) -> bool:
    success = True
    func = f"{__name__}.send_alert"

    post_event(
        "log_debug",
        f"{func}",
        f"Sending video alert with the level: {alert_template['level']}",
    )
    video_alert = VideoAlert()
    video_alert.alertMessage = alert_template["message"]
    if alert_template["level"] != "INFO" and alert_template["level"] != "DEBUG":
        # then there is a problem.
        post_event(
            "log_info",
            f"{func}",
            f"Requesting Email and Text because of the level: {alert_template['level']}",
        )
        video_alert.sendEmail = True
        video_alert.sendText = True

    video_alert.set_body()
    video_alert.send_alert()

    return success
