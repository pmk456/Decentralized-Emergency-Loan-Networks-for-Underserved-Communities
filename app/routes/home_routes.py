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
    # TODO
    return render_template("borrower/login.html")

@home_routes.route("/lender-login", methods=["GET", "POST"])
def lender_login():
    # TODO
    return render_template("lender/login.html")

# Signup routes for both lender & borrower


@home_routes.route("/borrower-signup", methods=["GET", "POST"])
def borrower_signup():
    if request.method == "POST":
        
        # DEBUG PURPOSE CODE START
        
        app = create_app()
        
        with app.app_context() as context:
            db.session.query(Lender).delete()
            db.session.commit()
            
        del app
        
        
        # DEBUG PURPOSE CODE END
        
        
        
        
        lender_data = dict()
        lender_data['name'] = request.form.get("name")
        lender_data['phone_no'] = request.form.get("phone_no")
        # Checking for existing phone number        
        if Lender.query.get(lender_data['phone_no']):
            flash("Phone already exists.", "error") # REMOVE
            return redirect(url_for("home_routes.borrower_signup"))
        
        lender_data['dob'] = request.form.get("lender-dob")
        # lender_data['aadhar'] = request.form.get('lender-aadhar')
        
        # Writing to the database
        app = create_app()
        with app.app_context() as context:
            new_lender = Lender(
                phone_number=lender_data['phone_no'],
                name=lender_data['name'],
                # dob=lender_data['dob'],
                # aadhar=lender_data['aadhar'],
                trust_score="50"
            )

            db.session.add(new_lender)
            db.session.commit()
        
        # OTP generation and validation
        otp_handler = otp.OtpHandler()
        otp_handler.send_otp(lender_data['phone_no'])
        session["PHONE_NO"] = lender_data["phone_no"]
        session['USER_TYPE'] = "borrower"
        return render_template("auth/verify-otp.html")
    
    return render_template("borrower/signup.html")


@home_routes.route("/borrower-signup/kyc-verification", methods=["GET", "POST"])
def kyc_verification():
    if request.method == "POST":
        pass
        # TODO
    
    return render_template('borrower/kyc.html')





@home_routes.route("/lender-signup", methods=["GET", "POST"])
def lender_signup():
    if request.method == "POST":
        
        # DEBUG PURPOSE CODE START
        
        app = create_app()
        
        with app.app_context() as context:
            db.session.query(Lender).delete()
            db.session.commit()
            
        del app
        
        
        # DEBUG PURPOSE CODE END
        
        
        lender_data = dict()
        lender_data['name'] = request.form.get("name")
        lender_data['phone_no'] = request.form.get("phone_no")
        # Checking for existing phone number        
        if Lender.query.get(lender_data['phone_no']):
            flash("Phone already exists.", "error") # REMOVE
            return redirect(url_for("home_routes.lender_signup"))
        
        lender_data['dob'] = request.form.get("lender-dob")
        # lender_data['aadhar'] = request.form.get('lender-aadhar')
        
        # Writing to the database
        app = create_app()
        with app.app_context() as context:
            new_lender = Lender(
                phone_number=lender_data['phone_no'],
                name=lender_data['name'],
                # dob=lender_data['dob'],
                # aadhar=lender_data['aadhar'],
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
            return render_template("lender/dashboard.html")
    else:
        flash("Incorrect OTP. Please try again.", "error") # REMOVE
        return redirect(url_for("home_routes.verify_otp")) 
