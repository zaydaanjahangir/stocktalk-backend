from extensions import db
from models import *

def init_db(app):
    with app.app_context():
        db.create_all()
