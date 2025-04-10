from flask import request, Blueprint, session
from twilio.twiml.messaging_response import MessagingResponse
from app.models import Lender  # or whatever your user model is
from app import db, create_app

whatsapp_routes = Blueprint("whatsapp_routes", __name__)

@whatsapp_routes.route("/chat", methods=['POST'])
def whatsapp_bot():
    # Extract user's WhatsApp number
    full_number = request.values.get('From', '')  # Format: whatsapp:+919876543210
    phone_number = full_number.replace("whatsapp:", "").strip()

    # Query your DB using phone number
    lender = Lender.query.filter_by(phone_number=phone_number).first()

    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if not lender:
        msg.body("Sorry! You're not registered in our system. Please sign up first.")
        return str(resp)

    if session.get('MONEY_REQUESTED'):
        if incoming_msg.lower().rstrip().lstrip() == 'yes':
            app = create_app()
            with app.app_context() as context:
                lender = Lender.query.get("+917330644650")
                lender.req_id = "REQ" + phone_number[::-1][:5]
                lender.amount = session['MONEY']
                print(lender.req_id)
                print(lender.amount)
                msg.body(f"Your Money Request of *₹{lender.amount}* Has been sent to Lender *{lender.name} with Request Id {lender.req_id}!*")
                db.session.commit()
            return str(resp)

    if 'hello' in incoming_msg or 'hi' in incoming_msg:
        msg.body("Hey! I'm your TrustPay Bot. You can raise your loan request from here    *Team Alliance*.")
    elif 'loan' in incoming_msg.lower():
        incoming_msg = incoming_msg.replace("loan", "").rstrip().lstrip()
        money = int(incoming_msg)
        session['MONEY'] = money
        msg.body(f"You are Requesting an amount of {money}₹.\nAre You Sure ? (Yes/No)")
        session['MONEY_REQUESTED'] = True
    else:
        msg.body("Sorry, I didn't understand that.")

    return str(resp)
