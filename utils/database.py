from app import db
from models import User, User_Interests, Stock, Stock_Vectors, Swipe

def init_db():
    db.create_all()
    print("Database initialized.")

if __name__ == "__main__":
    init_db()
