import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Replace with your email and password
sender_email = "algomagic17@gmail.com"
sender_password = "xhhs uusx cdbd padp"

# Replace with the recipient's email
receiver_email = "nisargmparmar1709@gmail.com"

# Create the email message
msg = MIMEMultipart('alternative')
msg['Subject'] = "OTP Verification by AgloMAGIC"
msg['From'] = sender_email
msg['To'] = receiver_email

# Create the HTML body
html = """
<html>
<body style="font-family: sans-serif; background-color: #f5f5f5; color: #333; margin: 0; padding: 0;">
    <main class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
        <header style="background-color: #fec302; color: #fff; padding: 10px; text-align: center; border-top-left-radius: 5px; border-top-right-radius: 5px;">
            <h1 style="margin: 0; font-size: 24px;">Algo<span>MAGIC</span></h1>
        </header>
        <section style="padding: 20px;">
            <p>Hi John,</p>
            <p>You are receiving this email so we can confirm this email address for your account. To finish verifying
                your email address, click the button below or enter the provided code.</p>
            <button class="otp-button" style="background-color: #f5f5f5; color: #fff; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none;">Verify Email Address</button>
            <p>This link expires in 5 minutes.</p>
            <p>To verify manually, enter this code: <span class="otp-code"
                    style="color: var(--secondary-color); font-weight: bold;">541081</span></p>
            <p>If you did not request this email, please contact an administrator at <a
                    href="mailto:johndoe@okta.com">algomagic@gmail.com</a>.</p>
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

print("Email sent successfully!")
