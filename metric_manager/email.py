from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.utils.timezone import now
import uuid
import ssl
import smtplib
from .models import *
EMAIL_BODY = """
Hi,\n\nTo verify your fitbit reset password please use the following verification code:{}\n\n
If you did not request this code, please let us know.\n\nThanks,\nSerums Team
"""
EMAIL_HTML="""
<html>
    <body>
        <p>Hi,<br><br>
            To verify your fitbit reset password
            please use the following verification code:<br><br>
            <strong>{}</strong>
        </p>
        <p>If you did not request this code, please let us know.</p><br><br>
        <p>Thanks,<br>
        Serums Team</p>
    </body>
</html>
"""
def build_email_object(verification_code,fromaddr,toaddr):
    """
    Args:
        verification_type (str):
            The verification type , which is included as a key in settings.VERIFICATION_TYPES
            and settings.MODEL_MAPPING
        verification_code (str):
            The verification code that will be displayed in the email
        fromaddr (str):
            The email of the sender
        toaddr (str):
            The email of the receiver
    Returns:
        MIMEMultipart object with the message.
        Text built lives in views_utils.EMAIL_BODY,views_utils.EMAIL_HTML
    """
    msg = MIMEMultipart("alternative")
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Fitbit EPL449 Reset password"
    text = EMAIL_BODY.format(verification_code)
    html = EMAIL_HTML.format(verification_code)
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)
    return msg



def generate_verification_code():
    '''Generates a 6-chat verification code using the UUID module

        Returns:
            (str): The 6-char verification code
    '''
    return uuid.uuid4().hex[0:6]

def send_verification_email(email, verification_code):
    """
    Sends an email containing the verification_code to the username

    Args:
        email (str): The email address.
        verification_code (str): The verification code.
        verification_type (str): The verification type. Any of settings.VERIFICATION_TYPES.

    Raises:
        ApplicationError: Custom Exception with a message and a status code
    """
    fromaddr = settings.FROM_EMAIL
    username_row = FitbitUser.objects.filter(email=email).values('email', 'id')

    if not username_row:
        raise Exception
    toaddr = username_row[0].get('email')
    user_fk_id = username_row[0].get('id')
    password = settings.PASS_EMAIL
    msg = build_email_object(verification_code,fromaddr,toaddr)
    context = ssl.create_default_context()
    FitbitUser.objects.filter(email=email).update(reset_code=verification_code)
    #finally if everything was successful send the mail
    s = smtplib.SMTP("smtp-mail.outlook.com",587)
    s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls() #Puts connection to SMTP server in TLS mode
    s.ehlo()
    s.login(fromaddr, password)
    s.sendmail(fromaddr, toaddr, msg.as_string())
    s.quit()
