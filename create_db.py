from app.models import *
from app import create_app, db
app = create_app()
with app.app_context() as context:
    db.create_all()
    db.session.commit()