from flask import url_for, Blueprint, redirect, render_template

borrower_routes = Blueprint("borrower_routes", __name__)

@borrower_routes.route("/borrower/borrower-dashboard")
def borrower_dashboard():
    
    
    pass
