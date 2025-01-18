from flask import Flask
from flask_cors import CORS
from extensions import db, migrate
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import models to register them with Flask-Migrate
    with app.app_context():
        from models import User, User_Interests, Stock, Stock_Vectors, Swipe

    # Register blueprints
    # register_blueprints(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
