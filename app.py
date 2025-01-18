from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
CORS(app)

from routes.auth_routes import auth_bp
from routes.stock_routes import stock_bp
from routes.swipe_routes import swipe_bp

app.register_blueprint(auth_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(swipe_bp)

if __name__ == '__main__':
    app.run(debug=True)
