import random
import time
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

def generate_otp(email, otp_file):
    # Load the existing OTP data from the JSON file
    try:
        with open(otp_file, "r") as f:
            otp_data = json.load(f)
    except FileNotFoundError:
        otp_data = {}

    # Generate a random 4-digit OTP
    while True:
        otp = str(random.randint(1000, 9999))
        # Check if the OTP already exists
        for existing_email, existing_otp_data in otp_data.items():
            if existing_otp_data["otp"] == otp:
                # OTP already exists, generate a new one
                break
        else:
            # OTP is unique, store it in the JSON file
            otp_data[email] = {"otp": otp, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            with open(otp_file, "w") as f:
                json.dump(otp_data, f)
            return otp

def check_otp(email, otp, otp_file):
    # Load the existing OTP data from the JSON file
    try:
        with open(otp_file, "r") as f:
            otp_data = json.load(f)
    except FileNotFoundError:
        return False
    # Check if the OTP exists in the JSON file
    if email in otp_data:
        # Get the OTP generation time
        generation_time = datetime.strptime(otp_data[email]["time"], "%Y-%m-%d %H:%M:%S")
        # Calculate the time difference
        time_diff = datetime.now() - generation_time
        # Check if the time difference is more than 1 minute
        if time_diff > timedelta(minutes=3):
            # Remove the OTP from the JSON file
            del otp_data[email]
            with open(otp_file, "w") as f:
                json.dump(otp_data, f)
            return False
        # Check if the OTP matches
        if otp_data[email]["otp"] == otp:
            return True
    return False

def mail_sender(receiver_email, name, otp):

    try:

        # Replace with your email and password
        sender_email = "algomagic17@gmail.com"
        sender_password = "xhhs uusx cdbd padp"

        # Create the email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "OTP Verification by AgloMAGIC"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Create the HTML body
        html = f"""
        <html>
        <body style="font-family: sans-serif; background-color: #f5f5f5; color: #333; margin: 0; padding: 0;">
            <main class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
                <header style="background-color: #fec302; color: #fff; padding: 10px; text-align: center; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                    <h1 style="margin: 0; font-size: 24px;">Algo<span>MAGIC</span></h1>
                </header>
                <section style="padding: 20px;">
                    <p>Hi {name},</p>
                    <p>You are receiving this email so we can confirm this email address for your account. To finish verifying
                        your email address, click the button below or enter the provided code.</p>
                    <button class="otp-button" style="background-color: #f5f5f5; color: #fff; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none;">Verify Email Address</button>
                    <p>This link expires in 5 minutes.</p>
                    <p>To verify manually, enter this code: <span class="otp-code"
                            style="color: #fec302; font-weight: bold;">{otp}</span></p>
                    <p>If you did not request this email, please contact an administrator at <a
                            href="mailto:algomagic@gmail.com">algomagic17@gmail.com</a>.</p>
                </section>
                <footer
                    style="background-color: #302b63; color: #fff; padding: 10px; text-align: center; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;">
                    <p style="margin: 0; font-size: 12px;">This is an automatically generated message by AlgoMAGIC. Replies are
                        not monitored or answered.</p>
                </footer>
            </main>
        </body>

        </html>
        """

        # Attach the HTML part to the email
        part2 = MIMEText(html, 'html')
        msg.attach(part2)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, receiver_email, msg.as_string())

        return True

    except Exception as e:
        return False


def forgot_mail_sender(receiver_email, name, otp):
    
    try:

        # Replace with your email and password
        sender_email = "algomagic17@gmail.com"
        sender_password = "xhhs uusx cdbd padp"

        # Create the email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "OTP Verification by AgloMAGIC"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Create the HTML body
        html = f"""
            <html>
                <body style="font-family: sans-serif; background-color: #f5f5f5; color: #333; margin: 0; padding: 0;">
                    <main class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
                        <header style="background-color: #fec302; color: #fff; padding: 10px; text-align: center; border-top-left-radius: 5px; border-top-right-radius: 5px;">
                            <h1 style="margin: 0; font-size: 24px;">Algo<span>MAGIC</span></h1>
                        </header>
                        <section style="padding: 20px;">
                            <p>Hi {name},</p>
                            <p>It seems like you’ve requested to reset your password. To proceed, please use the one-time password (OTP) provided below.</p>
                            
                            <p>Enter this OTP to reset your password:</p>
                            <p style="font-size: 20px; font-weight: bold; color: #fec302; text-align: center;">{otp}</p>

                            <p>This OTP is valid for the next 5 minutes. If you did not request a password reset, please ignore this email or contact our support team.</p>
                            
                            <p>If you encounter any issues, feel free to reach out to us at <a href="mailto:algomagic17@gmail.com">algomagic17@gmail.com</a>.</p>
                        </section>
                        <footer style="background-color: #302b63; color: #fff; padding: 10px; text-align: center; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;">
                            <p style="margin: 0; font-size: 12px;">This is an automated message from AlgoMAGIC. Please do not reply directly to this email.</p>
                        </footer>
                    </main>
                </body>
            </html>
        """

        # Attach the HTML part to the email
        part2 = MIMEText(html, 'html')
        msg.attach(part2)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, receiver_email, msg.as_string())

        return True

    except Exception as e:
        return False