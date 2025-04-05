"""
Author: Patan Musthakheem
Date & Time: 05-04-2024
"""
from flask import Blueprint, render_template, request, session, redirect
from flask import url_for

from .. import otp, db


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
        # TODO CHECK Whether already this phone no exists in db
        
        
        
        lender_data['dob'] = request.form.get("lender-dob")
        lender_data['aadhar'] = request.form.get('lender-aadhar')
        # TODO: Generate otp and verify it
        otp_handler = otp.OtpHandler()
        otp_data = otp_handler.send_otp(lender_data['phone_no'])
        db.write_otp(lender_data['phone_no'], otp_data)
        return render_template("auth/verify-otp.html")
    
    return render_template("lender/signup.html")


from flask import flash

@home_routes.route("/verify-otp", methods=["POST"])
def verify_otp():
    user_otp = request.form.get("otp")

    if not session.get("PHONE_NO") or not user_otp:
        flash("Session expired or OTP missing. Please try again.", "error")
        return redirect(url_for("home_routes.lender_signup"))

    stored_otp = db.get_otp(session['PHONE_NO'])

    if stored_otp == user_otp:
        flash("OTP verified successfully!", "success")
        return redirect(url_for("home_routes.lender_dashboard"))  # You can change this route as needed
    else:
        flash("Incorrect OTP. Please try again.", "error")
        return redirect(url_for("home_routes.verify_otp_form"))  # Make sure this route exists
