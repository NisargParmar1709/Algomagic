# import random
# import time
import json
# from datetime import datetime, timedelta

# # JSON file to store OTP data
# otp_file = "otp_data.json"

# def generate_otp(email):
#     # Load the existing OTP data from the JSON file
#     try:
#         with open(otp_file, "r") as f:
#             otp_data = json.load(f)
#     except FileNotFoundError:
#         otp_data = {}

#     # Generate a random 4-digit OTP
#     while True:
#         otp = str(random.randint(1000, 9999))
#         # Check if the OTP already exists
#         for existing_email, existing_otp_data in otp_data.items():
#             if existing_otp_data["otp"] == otp:
#                 # OTP already exists, generate a new one
#                 break
#         else:
#             # OTP is unique, store it in the JSON file
#             otp_data[email] = {"otp": otp, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
#             with open(otp_file, "w") as f:
#                 json.dump(otp_data, f)
#             return otp

# def check_otp(email, otp):
#     # Load the existing OTP data from the JSON file
#     try:
#         with open(otp_file, "r") as f:
#             otp_data = json.load(f)
#     except FileNotFoundError:
#         return False
#     # Check if the OTP exists in the JSON file
#     if email in otp_data:
#         # Get the OTP generation time
#         generation_time = datetime.strptime(otp_data[email]["time"], "%Y-%m-%d %H:%M:%S")
#         # Calculate the time difference
#         time_diff = datetime.now() - generation_time
#         # Check if the time difference is more than 1 minute
#         if time_diff > timedelta(minutes=3):
#             # Remove the OTP from the JSON file
#             del otp_data[email]
#             with open(otp_file, "w") as f:
#                 json.dump(otp_data, f)
#             return False
#         # Check if the OTP matches
#         if otp_data[email]["otp"] == otp:
#             return True
#     return False

# i = 0

# while True:
# 	# Example usage
# 	email = f"user{i}@example.com"
# 	otp = generate_otp(email)
# 	i += 1
# 	print(f"{i}. Generated OTP for {email}: {otp}")

# 	# Simulate a delay of 2 minutes
# 	time.sleep(2)

# 	# Try to check the OTP
# 	if check_otp(email, otp):
# 		print("OTP is valid")
# 	else:
# 		print("OTP is invalid or expired")

otp_file = "otp_data.json"

with open(otp_file, "r") as f:
	otp_data = json.load(f)

for email in otp_data:
	print(otp_data[email]["otp"])