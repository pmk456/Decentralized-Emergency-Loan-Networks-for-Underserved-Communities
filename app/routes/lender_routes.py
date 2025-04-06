from flask import Blueprint, render_template

lender_routes = Blueprint("lender_routes", __name__)

@lender_routes.route("/lender/lender-dashboard")
def lender_dashboard():
    
    return render_template("lender/dashboard.html")


