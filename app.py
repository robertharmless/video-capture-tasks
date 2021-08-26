"""
Video Capture Processing app
"""

# Built-in
from sys import argv as args

# Special

# App
from api.event import post_event
from api.log_listener import setup_log_event_handlers
from api.email_listener import setup_email_event_handlers
from api.alert_listener import setup_alert_event_handlers
from lib.config import App
from lib.email import generate_email_templates
from lib import file
from lib.metadata import Metadata
from lib.utilities import Timer

app = App()
setup_log_event_handlers()
setup_email_event_handlers()
setup_alert_event_handlers()


def main():

    func = f"{__name__}.main"

    post_event("log_info", f"{func}", f"Received the system args:{args}.")

    for arg in args:
        post_event("log_info", f"{func}", f"Received the arg:{arg}.")

    metadata = Metadata(args)

    # script and process related variables
    metadata.script_start_time = timer.start

    post_event("log_info", f"{func}", f"The basic metadata:{metadata}")

    if metadata.alert_type == "end":
        metadata = file.move_to_complete(metadata)

    generated_template = generate_email_templates(metadata)

    post_event("send_email", f"{func}", data=generated_template)

    alert_template = {"level": "DEBUG", "message": "alert message"}
    post_event("send_teams_alert", f"{func}", alert_template)

    return True


if __name__ == "__main__":
    func = f"{__name__}"
    timer = Timer()

    post_event("log_info", f"{func}", "Script is beginning.")

    try:
        data = main()

    except Exception as ex:
        post_event("log_exception", f"{func}", f"Error from Main:{ex}")

    message = timer.finished()
    post_event("log_info", f"{func}", message)

    post_event("log_info", f"{func}", "Script is complete.")
