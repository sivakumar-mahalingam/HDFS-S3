import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
from logger_setting import *

def send_mail(ex_msg):
    py_logger = logging.getLogger('py_logger')

    try:
        config_path = '/edgenode/s3/download/s3_config.conf'
        configuration_file = configparser.ConfigParser()
        config = configuration_file.read_file(open(config_path))

        receiver_email=configuration_file.get('config', 'receiver_email').split(',')

        message = MIMEMultipart("alternative")
        message["Subject"] = configuration_file.get('config', 'email_subject')
        message["From"] = configuration_file.get('config', 'sender_email')
        message["To"] = ", ".join(receiver_email)

        # Create the HTML version of your message
        html = """\
        <html>
          <body>
            <p>Hi,<br><br>
               <b>Exception Occurred in application """ + configuration_file.get('config', 'mail_app_name') + """</b><br>
               Exception :<br>"""\
               + str(ex_msg) + """\
            </p>
          </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        message_part = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(message_part)

        server = smtplib.SMTP(configuration_file.get('config', 'smtp_server_name'))
        server.sendmail(configuration_file.get('config', 'sender_email'),
                        receiver_email,
                        message.as_string())

    except Exception as e:
        py_logger.error(e)
