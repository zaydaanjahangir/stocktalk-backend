from flask import Flask
from flask_cors import CORS
from extensions import db, migrate
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.stock_routes import stock_bp
from routes.swipe_routes import swipe_bp


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

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(stock_bp, url_prefix='/api/stocks')
    app.register_blueprint(swipe_bp, url_prefix='/api/swipes')


    return app
3 
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
