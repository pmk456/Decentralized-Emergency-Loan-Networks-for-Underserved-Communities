"""
Author: Patan Musthakheem
Date & Time: 05-04-2024
Updated to use Twilio Verify API
"""

import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
VERIFY_SERVICE_SID = os.getenv("TWILIO_VERIFY_SERVICE_SID")

class OtpHandler:
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        print("Twilio Verify Client initialized!")

    def send_otp(self, phone_number: str):
        """ Sends OTP to the user's phone via Twilio Verify """
        try:
            verification = self.client.verify.v2.services(VERIFY_SERVICE_SID) \
                .verifications \
                .create(to=phone_number, channel='sms')
            print(f"OTP sent to {phone_number}, Status: {verification.status}")
        except Exception as e:
            print(f"Error sending OTP: {e}")

    def validate_otp(self, phone_number: str, otp: str):
        """ Validates entered OTP using Twilio Verify """
        try:
            verification_check = self.client.verify.v2.services(VERIFY_SERVICE_SID) \
                .verification_checks \
                .create(to=phone_number, code=otp)
            if verification_check.status == "approved":
                print(f"OTP verified for {phone_number}")
                return True
            else:
                print(f"Invalid OTP for {phone_number}")
                return False
        except Exception as e:
            # print(f"Error verifying OTP: {e}")
            return False
