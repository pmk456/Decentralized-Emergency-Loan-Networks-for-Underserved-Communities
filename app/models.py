"""
Author: Patan Musthakheem
Date & Time: 05-04-2024
"""
from app import db
import datetime

class Lender(db.Model):    
    phone_number = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100))
    aadhar = db.Column(db.String(100))
    trust_score = db.Column(db.String(10))
    
class Borrower(db.Model):
    phone_number = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    trust_score = db.Column(db.Float)
    kyc_status = db.Column(db.Boolean)

class Loan(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    lender_id = db.Column(db.String, db.ForeignKey('lender.phone_number'))
    borrower_id = db.Column(db.String, db.ForeignKey('borrower.phone_number'))
    amount = db.Column(db.Float)
    status = db.Column(db.String(50))
    
    
class Ledger(db.Model):
    __tablename__ = 'ledger'

    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.loan_id'))
    action = db.Column(db.String(50)) 
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    amount = db.Column(db.Float)
    hash = db.Column(db.String(128)) # hash to be stored

class OTP(db.Model):
    __tablename__ = 'otp'

    phone_number = db.Column(db.String, primary_key=True)
    otp_code = db.Column(db.String(6))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)