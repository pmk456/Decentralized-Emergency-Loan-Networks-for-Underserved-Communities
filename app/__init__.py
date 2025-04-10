import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Build the absolute path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'db', 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes.home_routes import home_routes
    from .routes.lender_routes import lender_routes
    from .routes.whatsapp_api import whatsapp_routes
    app.register_blueprint(home_routes)
    app.register_blueprint(lender_routes)
    app.register_blueprint(whatsapp_routes)
    return app



"""

insert_data = {
    "loan_id": 42,
    "action": "payment_received",
    "amount": 1000.0,
    "hash": "abc123hash456"
}

response = update_ledger(insert_data, delete_entry_id=7)
print(response)"""