"""
Author: Patan Musthakheem
Date & Time: 05-04-2024
"""
import random
import os
import requests

from .models import OTP
from app import db, create_app
API_KEY = os.getenv("TWO_FACTOR_API_KEY")  
SENDER_ID = "TXTIND"

class OtpHandler:
    def __init__(self):
        app = create_app()
        with app.app_context() as context:
            db.session.query(OTP).delete()
            db.session.commit()
            print("Reset OTP Codes!")
    
    def _generate_otp(self):
        return str(random.randint(100000, 999999))

    def send_otp(self, number: str):
        otp = self._generate_otp()
        self._send(otp, number)
        self._write_otp(number, otp)

    def _send(self, otp, number):
        url = f"https://2factor.in/API/V1/{API_KEY}/SMS/{number}/{otp}/{SENDER_ID}"
        requests.get(url)

    def _write_otp(self, number, otp):
        """ Write the OTP to the database """
        app = create_app()
        with app.app_context():
            otp_entry = OTP(phone_number=number, otp_code=otp)
            db.session.add(otp_entry)
            db.session.commit()

    def validate_otp(self, phone_no, entered_otp):
        """ Fetch OTP from db and compare here"""
        return True
        # ORDER: REWRITE THE CODE
        
        
        # app = create_app()
        # with app.app_context():
        #     latest_otp = OTP.query.filter_by(phone_number=phone_no).order_by(OTP.timestamp.desc()).first()
        #     print("Latest otp ", latest_otp)
        #     if latest_otp is not None:
        #         print("latest otp code ", latest_otp.code)
        #         if latest_otp.otp_code == entered_otp:
        #             self._remove_otp(phone_no)
        #             return True
        # return False
            
    def _remove_otp(self, number):
        """ Remove OTP from database after successful verification """
        app = create_app()
        with app.app_context():
            otp_entry = OTP.query.filter_by(phone_number=number).first()
            if otp_entry:
                db.session.delete(otp_entry)
                db.session.commit()
                print(f"OTP for phone number {number} removed from the database.")
            else:
                print(f"No OTP found for phone number {number}.")
