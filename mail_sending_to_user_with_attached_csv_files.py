## Imports

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.message import Message
from email.mime.text import MIMEText

## Mail Sending function

def mailsend(emailto):
    try:
        # Mail details
        emailfrom = "elvistitus5@gmail.com"
        fileToSend = ["Full Comments.csv", "Positive_Comments.csv", "Negative_Comments.csv"]
        username = "elvistitus5@gmail.com"
        password = "udvbimgzzenpcizt"

        # Mail Subject
        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = emailto
        msg["Subject"] = "Hi your youtube comments excel file is here   -Youtube Comment Scraper"

        # Adding attachments
        subtype = 'vnd.ms-excel'  # Subtype for excel or csv files
        for f in fileToSend:
            fp = open(f, encoding='utf8')
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
            attachment.add_header("Content-Disposition", "attachment", filename=f)
            msg.attach(attachment)

        # Sending mail to the user
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username, password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
    except Exception as e:
        # Log the error message
        print(f"An error occurred while sending email: {e}")
        raise  # Reraise the exception to propagate the error to the caller

