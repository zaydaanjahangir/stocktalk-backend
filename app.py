from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # Error handling
    @app.errorhandler(Exception)
    def handle_exception(e):
        return {"status": "error", "message": str(e)}, 500

    # Health check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {"status": "ok"}, 200

    # Register blueprints
    from routes.user_routes import user_bp
    from routes.stock_routes import stock_bp
    from routes.swipe_routes import swipe_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(swipe_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
