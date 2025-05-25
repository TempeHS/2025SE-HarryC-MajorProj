import pyotp
import random
import smtplib
from email.mime.text import MIMEText



def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_email(admin_email, otp_code):
    # Set up the email server
    msg = MIMEText(f"Your verification code is: {otp_code}")
    msg['Subject'] = "Your 2FA Verification Code"
    msg['From'] = "leacupuncturetest@gmail.com"
    msg['To'] = admin_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("leacupuncturetest@gmail.com", "pjpg wihe vhsc kkiw")
        server.send_message(msg)

def verify_otp(user_input, otp_code):
    if user_input == otp_code:
        return True
    else:
        return False