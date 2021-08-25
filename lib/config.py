"""
Configuration Settings.
"""
# Built-in
from os import environ
from os.path import join, expanduser, exists
import socket

# App
from api.event import post_event


class App:
    """
    App configs
    """

    hostname = None
    appname = "video capture processing"

    # email related variables
    email_server_ip = None
    email_server_port = None
    email_to = None
    sender_email = None

    # templates
    email_template_file = None
    snippet_contact_support_file = None
    snippet_email_style = None
    snippet_teams_support = None

    # teams related variables
    video_alert_url = None
    teams_alert_to = None

    # folders
    capture_folder_name = None
    destination_folder_name = None

    def __init__(self):
        func = f"{__name__}.{__class__}.__init__"

        self.hostname = socket.gethostname()

        self.email_server_ip = environ["EMAIL_SERVER_IP"]
        self.email_server_port = environ["EMAIL_SERVER_PORT"]
        self.email_to = environ["EMAIL_TO"].split(",")
        self.sender_email = f"Video Capture Alert<just_in_alert@{self.hostname}>"

        self.video_alert_url = environ["VIDEO_ALERT_URL"]
        self.teams_alert_to = environ["TEAMS_ALERT_TO"].split(",")

        self.capture_folder_name = environ["CAPTURE_FOLDER_NAME"]
        self.destination_folder_name = environ["DESTINATION_FOLDER_NAME"]

        email_alert_filename = environ["CAPTURE_FOLDER_NAME"]
        snippet_email_style_filename = environ["SNIPPET_EMAIL_STYLE_FILENAME"]
        snippet_contact_support_filename = environ["SNIPPET_CONTACT_SUPPORT_FILENAME"]
        snippet_teams_support_filename = environ["SNIPPET_TEAMS_SUPPORT"]

        self.email_template_file = f"./templates/{email_alert_filename}"
        self.snippet_email_style = f"./templates/{snippet_email_style_filename}"
        self.snippet_contact_support_file = (
            f"./templates/{snippet_contact_support_filename}"
        )
        self.snippet_teams_support = f"./templates/{snippet_teams_support_filename}"

        post_event("log_debug", f"{func}", f"Email templates loaded.")


class Logs(object):
    """
    Logging configs
    """

    loglevel = 10

    log_folder = None
    log_filename = None
    log_file_path = None

    def __init__(self):
        app = App()
        func = f"{__name__}"

        # NOTSET=0, DEBUG=10, INFO=20, WARN=30, ERROR=40, and CRITICAL=50
        self.loglevel = int(environ["LOGLEVEL"] if environ["LOGLEVEL"] != None else 10)

        self.log_filename = f"{app.appname}.log"
        self.log_folder = f"{expanduser('~')}/Library/Logs/"

        # Verify log file exists
        self.log_file_path = join(self.log_folder, self.log_filename)

        if exists(self.log_file_path):
            # do something
            print("log exists")

        else:
            # create one
            with open(self.log_file_path, "w") as fp:
                post_event(
                    "log_debug", f"{func}", f"Created the log file:{self.log_filename}."
                )
                pass
