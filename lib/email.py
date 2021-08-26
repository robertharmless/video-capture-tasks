"""
Email Processes
"""
# Built-in
from lib.metadata import Metadata
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Special

# App
from api.event import post_event
from .config import App

app = App()


def generate_email_templates(metadata: Metadata):

    renamed_text = ""
    if metadata.alert_type == "True":
        renamed_text = "[ File was renamed ]<br>"

    email_subject = "Video Alert"
    headline = "Video Alert"
    email_subject_sm = "Video Alert"

    if metadata.alert_type == "start":
        email_subject = f"Capture Beginning: {metadata.clipname}"
        email_subject_sm = "Capture Beginning"
        headline = f"JustIn has begun recording:"
        metadata.capture_duration = "-"
        metadata.inpoint = "-"
        metadata.outpoint = "-"

    elif metadata.alert_type == "end":
        email_subject = f"Capture Complete: {metadata.clipname}"
        email_subject_sm = "Capture Complete"
        headline = f"JustIn has finished recording:"

    else:
        email_subject = "Video Alert"
        email_subject_sm = "Video Alert"
        headline = "This is a video alert."

    # set the text template
    email_text = f"""\
        Hello,

        {headline}
        file name: {metadata.clipname}
        {renamed_text}

        -Just:In Monitor"""

    # set the html template
    with open(app.email_alert_template_file) as f:
        template = f.read()

    email_style_snippet = generate_email_style_snippet()
    teams_support_snippet = generate_teams_support_snippet()
    contact_support_snippet = generate_contact_support_snippet()

    email_html = (
        template.replace("%email_style%", f"{email_style_snippet}")
        .replace("%teams_support_snippet%", f"{teams_support_snippet}")
        .replace("%contact_support_snippet%", f"{contact_support_snippet}")
        .replace("%logo_svg_url%", f"{app.logo_svg_url}")
        .replace("%email_subject_sm%", f"{email_subject_sm}")
        .replace("%headline%", f"{headline}")
        .replace("%clipname%", f"{metadata.clipname}")
        .replace("%renamed_text%", f"{renamed_text}")
        .replace("%framerate%", f"{metadata.framerate}")
        .replace("%full_clipname%", f"{metadata.full_clipname}")
        .replace("%capture_codec%", f"{metadata.capture_codec}")
        .replace("%audio_channels%", f"{metadata.audio_channels}")
        .replace("%capture_resolution%", f"{metadata.capture_resolution}")
        .replace("%capture_duration%", f"{metadata.capture_duration}")
        .replace("%inpoint%", f"{metadata.inpoint}")
        .replace("%outpoint%", f"{metadata.outpoint}")
        .replace("%hostname%", f"{app.hostname}")
        .replace("%script_start_time%", f"{metadata.script_start_time}")
    )

    return {
        "email_html": email_html,
        "email_text": email_text,
        "email_subject": email_subject,
    }


def generate_email_style_snippet():

    with open(app.snippet_email_style_file) as f:
        email_style_snippet = f.read()

    return email_style_snippet


def generate_teams_support_snippet():

    with open(app.snippet_teams_support_file) as f:
        template = f.read()

    teams_support_snippet = template.replace(
        "%support_teams_link%", f"{app.support_teams_link}"
    )

    return teams_support_snippet


def generate_contact_support_snippet():

    with open(app.snippet_contact_support_file) as f:
        template = f.read()

    contact_support_snippet = (
        template.replace("%support_contact1_name%", f"{app.support_contact1_name}")
        .replace("%support_contact1_phone%", f"{app.support_contact1_phone}")
        .replace("%support_contact1_email%", f"{app.support_contact1_email}")
    )

    return contact_support_snippet


def send_email(who: str, generated_template: dict):
    func = f"{__name__}.send_email"
    # send the email

    receiver_emails = app.email_to

    message = MIMEMultipart("alternative")
    message["Subject"] = generated_template["email_subject"]
    message["From"] = app.sender_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(generated_template["email_text"], "plain")
    part2 = MIMEText(generated_template["email_html"], "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    for receiver in receiver_emails:

        post_event(
            "log_info",
            f"{func}",
            f"The email receiver is [{type(receiver)}]:{receiver}.",
        )

        message["To"] = receiver

        # Create secure connection with server and send email
        with smtplib.SMTP(
            f"{app.email_server_ip}", f"{app.email_server_port}"
        ) as server:
            server.sendmail(app.sender_email, receiver, message.as_string())

        post_event("log_info", f"{func}", f"Email(s) have been sent to:{receiver}.")

    return True
