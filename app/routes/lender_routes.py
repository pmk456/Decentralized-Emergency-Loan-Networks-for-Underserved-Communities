from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from .. import create_app, db
from ..models import Lender
from ..payment import Payment
import os
lender_routes = Blueprint("lender_routes", __name__)


@lender_routes.route("/lender/lender-dashboard", methods=["GET","POST"])
def lender_dashboard():
    USER_ID = session.get("USER_ID")
    if not USER_ID:
        return redirect(url_for("home_routes.lender_login"))
    
    app = create_app()
    with app.app_context() as context:
        user_details = Lender.query.get(USER_ID)
        user_data = {
            'name': user_details.name,
            'phone_no': USER_ID,
            'trust_score': user_details.trust_score,
            'wallet_balance': user_details.wallet_balance
            
        }
        if user_details.req_id is not None:
            user_data['req_id'] = user_details.req_id
        if user_details.amount is not None:    
            user_data['amount'] = user_details.amount
    
    return render_template("lender/dashboard.html",
                           user_data=user_data)


@lender_routes.route("/create_order", methods=["POST"])
def create_payment():
    try:
        data = request.get_json()
        amount = int(data.get("amount", 0))
        if amount <= 0:
            return jsonify({"error": "Invalid amount"}), 400
        payment = Payment()
        order_id = payment.create_payment(amount * 100)  # convert rupees to paise
        session['amount'] = amount
        return jsonify({
            "order_id": order_id,
            "amount": amount * 100,
            "currency": "INR",
            "key": "rzp_test_DG2hG9ikul7Let"  # expose only public key
        })
    except Exception as e: 
        return jsonify({"error": str(e)}), 500


@lender_routes.route("/lender/lender-dashboard/payment-completed", methods=["POST"])
def payment_completed():
    app = create_app()
    with app.app_context():
        user_id = session.get("USER_ID")

        if not user_id:
            return jsonify({"error": "User not logged in"}), 401

        amount_added = session['amount']
        
        
        if not amount_added or int(amount_added) <= 0:
            return jsonify({"error": "Invalid amount"}), 400

        # Fetch the lender from DB
        lender = Lender.query.get(user_id)

        if not lender:
            return jsonify({"error": "Lender not found"}), 404

        # Update wallet balance
        lender.wallet_balance += int(amount_added)
        # Commit to database
        db.session.commit()
        return redirect(url_for("lender_routes.lender_dashboard"))
    
from twilio.rest import Client
@lender_routes.route("/completed-everything")
def send_whatsapp_message():
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("AUTH_TOKEN")
    from_whatsapp_number = 'whatsapp:+14155238886'  # Twilio sandbox number or your approved number
    to_whatsapp_number = f'whatsapp:{"+917330644650"}'  # e.g., whatsapp:+917330644650
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Hey, Mahima Your Loan Is Approved, Intiating Transaction of ₹500 to Your Account!",
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
    return message.sid

        

