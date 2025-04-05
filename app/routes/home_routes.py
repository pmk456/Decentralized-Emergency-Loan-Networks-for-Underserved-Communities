"""
Author: Patan Musthakheem
Date & Time: 05-04-2024
"""
from flask import Blueprint, render_template, request, session, redirect
from flask import url_for, flash

from .. import otp, db
from ..models import Lender, Borrower, OTP
from .. import create_app

home_routes = Blueprint('home_routes', __name__)  


# Home Page

@home_routes.route("/")
def home():
    return render_template("home.html")

@home_routes.route("/borrower-login", methods=["GET", "POST"])
def borrower_login():
    # TODO
    return render_template("borrower/signup.html")

@home_routes.route("/lender-login", methods=["GET", "POST"])
def lender_login():
    # TODO
    return render_template("borrower/login.html")

# Signup routes for both lender & borrower


@home_routes.route("/borrower-signup", methods=["GET", "POST"])
def borrower_signup():
    # TODO
    return render_template("borrower/signup.html")


@home_routes.route("/lender-signup", methods=["GET", "POST"])
def lender_signup():
    # TODO
    if request.method == "POST":
        lender_data = dict()
        lender_data['name'] = request.form.get("lender-name")
        lender_data['phone_no'] = request.form.get("lender-phone")
        # TODO Check Whether already this phone no exists in db
        
        if Lender.query.get(lender_data['phone_no']):
            flash("Phone already exists.", "error")
            return redirect(url_for("home_routes.lender-signup"))
        
        lender_data['dob'] = request.form.get("lender-dob")
        lender_data['aadhar'] = request.form.get('lender-aadhar')
        # Writing to the database
        app = create_app()
        with app.app_context as context:
            new_lender = Lender(
                name=db['name'],
                phone_number=db['phone_no'],
                aadhar=db['aadhar'],
                trust_score=50
            )

            db.session.add(new_lender)
            db.session.commit()
        
        # TODO: Generate otp and verify it ---> DONE
        otp_handler = otp.OtpHandler()
        otp_handler.send_otp(lender_data['phone_no'])
        session["PHONE_NO"] = lender_data["phone_no"]
        return render_template("auth/verify-otp.html")
    
    return render_template("lender/signup.html")



@home_routes.route("/signup/verify-otp", methods=["POST"])
def verify_otp():
    user_otp = request.form.get("otp")
    if not session.get("PHONE_NO") or not user_otp:
        flash("Session expired or OTP missing. Please try again.", "error")
        return redirect(url_for("home_routes.lender-signup"))
    handler = otp.OtpHandler()
    validate = handler.validate_otp(session['PHONE_NO'], user_otp)

    if validate:
        flash("OTP verified successfully!", "success")
        return redirect(url_for("home_routes.lender_dashboard")) 
    else:
        flash("Incorrect OTP. Please try again.", "error")
        return redirect(url_for("home_routes.verify-otp")) 
