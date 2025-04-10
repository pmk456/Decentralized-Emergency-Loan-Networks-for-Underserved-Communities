"""
Author: Patan Musthakheem
Date & Time: 05-04-2024
"""
from flask import Blueprint, render_template, request, session
from flask import url_for, flash, redirect

from .. import otp, db
from ..models import Lender, Borrower
from .. import create_app

home_routes = Blueprint('home_routes', __name__)  


# Home Page

@home_routes.route("/")
def home():
    return render_template("home.html")

@home_routes.route("/borrower-login", methods=["GET", "POST"])
def borrower_login():
    if request.method == "POST":
        phone_no = request.form.get("phone_no")
        password = request.form.get("password")
        if not phone_no or not password:
            flash("Please Enter Details!", "error")
            return redirect(url_for("home_routes.borrower_login"))
        # STATIC LOGIN FOR NOW, Encryption will be implemented later
        if phone_no != "+917330644650" or password != "1219":
            flash("Please Enter Correct Details!", "error")
            return redirect(url_for("home_routes.borrower_login"))
                
        return render_template("borrower/dashboard.html")
    return render_template("borrower/login.html")
    
    
    
@home_routes.route("/lender-login", methods=["GET", "POST"])
def lender_login():
    if request.method == "POST":
        phone_no = request.form.get("phone_no")
        password = request.form.get("password")
        if not phone_no or not password:
            flash("Please Enter Details!", "error")
            return redirect(url_for("home_routes.lender_login"))
        # STATIC LOGIN FOR NOW, Encryption will be implemented later
        if phone_no != "+917330644650" or password != "1219":
            flash("Please Enter Correct Details!", "error")
            return redirect(url_for("home_routes.lender_login"))
        session['USER_ID'] = phone_no
        return redirect(url_for("lender_routes.lender_dashboard"))
    return render_template("lender/login.html")

# Signup routes for both lender & borrower


@home_routes.route("/borrower-signup", methods=["GET", "POST"])
def borrower_signup():
    if request.method == "POST":        
        borrower_data = dict()
        borrower_data['name'] = request.form.get("name")
        borrower_data['phone_no'] = request.form.get("phone_no")
        # Checking for existing phone number        
        if Lender.query.get(borrower_data['phone_no']):
            flash("Phone already exists.", "error") # REMOVE
            return redirect(url_for("home_routes.borrower_signup"))
        
        borrower_data['dob'] = request.form.get("lender-dob")
        
        # Writing to the database
        app = create_app()
        with app.app_context() as context:
            new_lender = Borrower(
                phone_number=borrower_data['phone_no'],
                name=borrower_data['name'],
                trust_score="50"
            )

            db.session.add(new_lender)
            db.session.commit()
        
        # OTP generation and validation
        otp_handler = otp.OtpHandler()
        otp_handler.send_otp(borrower_data['phone_no'])
        session["PHONE_NO"] = borrower_data["phone_no"]
        session['USER_TYPE'] = "borrower"
        return render_template("auth/verify-otp.html")
    
    return render_template("borrower/signup.html")


@home_routes.route("/borrower-signup/kyc-verification", methods=["GET", "POST"])
def kyc_verification():
    if request.method == "POST":
        kyc_data = {
            'name': request.form.get('username'),
            'phone_no': request.form.get("phone_no"),
            'dob': request.form.get("dob"),
            'aadhar_no': request.form.get('aadhar_no')
        }
        # Accept Uploaded Document
        # TODO LEAVE THIS FOR NOW
        
    
    return render_template('borrower/kyc.html')





@home_routes.route("/lender-signup", methods=["GET", "POST"])
def lender_signup():
    if request.method == "POST":    
        lender_data = dict()
        lender_data['name'] = request.form.get("name")
        lender_data['phone_no'] = request.form.get("phone_no")
        # Checking for existing phone number        
        if Lender.query.get(lender_data['phone_no']):
            flash("Phone already exists.", "error") # REMOVE
            return redirect(url_for("home_routes.lender_signup"))
        
        lender_data['dob'] = request.form.get("lender-dob")        
        # Writing to the database
        app = create_app()
        with app.app_context() as context:
            new_lender = Lender(
                phone_number=lender_data['phone_no'],
                name=lender_data['name'],
                wallet_balance=0,
                trust_score="50"
            )

            db.session.add(new_lender)
            db.session.commit()
        
        # OTP generation and validation
        otp_handler = otp.OtpHandler()
        otp_handler.send_otp(lender_data['phone_no'])
        session["PHONE_NO"] = lender_data["phone_no"]
        session['USER_TYPE'] = "lender"
        return render_template("auth/verify-otp.html")
    
    return render_template("lender/signup.html")



@home_routes.route("/signup/verify-otp", methods=["POST"])
def verify_otp():
    user_otp = request.form.get("otp")
    if not session.get("PHONE_NO") or not user_otp:
        flash("Session expired or OTP missing. Please try again.", "error")
        return redirect(url_for("home_routes.lender_signup"))
    handler = otp.OtpHandler()
    validate = handler.validate_otp(session['PHONE_NO'], user_otp)
    if validate:
        flash("OTP verified successfully!", "success") # REMOVE
        if session['USER_TYPE'] == 'borrower':
            return render_template("borrower/kyc.html")
        elif session['USER_TYPE'] == 'lender':
            return redirect(url_for('lender_routes.lender_dashboard'))
    else:
        flash("Incorrect OTP. Please try again.", "error") # REMOVE
        return redirect(url_for("home_routes.verify_otp")) 
