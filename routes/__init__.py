from flask import Flask
from .stock_routes import stock_bp
from .swipe_routes import swipe_bp

def register_blueprints(app: Flask):
    app.register_blueprint(stock_bp)
    app.register_blueprint(swipe_bp)
