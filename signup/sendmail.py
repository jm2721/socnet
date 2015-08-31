    # Import smtplib for the actual sending function
import smtplib
import random

# Import the email modules we'll need
from email.mime.text import MIMEText

def generate_code():
    random.seed()
    string = ""
    for i in range(10):
        bins = [random.randint(65, 90), random.randint(97, 122), random.randint(48, 57)]
        whichbin = random.randint(0, 100)
        if whichbin < 80:
            char = random.choice(bins[0:2])
        else:
            char = random.choice(bins[2:3]) 
        string = string + chr(char)
    return string

def sendmail(email, code):
    msg = """From: From Person <jm2721@trevor.org>
To: To Person <{email}>
Subject: Confirm registration on socnet

Hello,
Go to socnet.com/activate and please input the code below and your username to finalize the registration.

Code: {code}
""".format(email=email, code=code)

    sender = 'jm2721@trevor.org'
    receivers = [email]

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('smtp.gmail.com')
    s.starttls()
    s.login('mailer2011280@gmail.com', 'thisisadummypassword')
    s.sendmail(sender, receivers, msg)
    s.quit()

if __name__ == "__main__":
    sendmail()
