import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sentence_transformers import SentenceTransformer
from app import create_app, db
from models import Stock, Stock_Vectors

# Initialize Flask app
app = create_app()

# Initialize scaler and text embedding model
scaler = MinMaxScaler()
model = SentenceTransformer('all-MiniLM-L6-v2')  # Pre-trained text embedding model


# Categories for each stock
stock_categories = {
    "AAPL": ["Tech", "Consumer Electronics", "Software"],
    "MSFT": ["Tech", "Software", "Cloud Computing"],
    "GOOGL": ["Tech", "Advertising", "AI"],
    "XOM": ["Energy", "Oil & Gas", "Petroleum"],
    "WMT": ["Retail", "Supermarkets", "Hypermarkets"],
    "TWLO": ["Tech", "Cloud Communications", "API"],
    "SAVE": ["Airlines", "Travel", "Leisure"],
    "CHGG": ["Tech", "Education", "E-Learning"],
    "NEM": ["Mining", "Gold", "Precious Metals"],
    "RUN": ["Energy", "Solar", "Renewable Energy"],
    "PLUG": ["Tech", "Fuel Cells", "Hydrogen"],
    "QS": ["Tech", "Electric Vehicles", "Batteries"],
    "CRSR": ["Tech", "Gaming", "Peripherals"],
    "STAG": ["Real Estate", "REIT", "Industrial"],
    "BCRX": ["Pharmaceuticals", "Biotech", "Drug Manufacturers"]
}

# Function to compute and store embeddings
def compute_and_store_vectors(tickers):
    with app.app_context():
        stocks = Stock.query.filter(Stock.ticker.in_(tickers)).all()

        # Prepare numerical data for normalization
        numerical_data = []
        for stock in stocks:
            numerical_data.append([
                stock.market_cap or 0,  # Handle None values
            ])

        # Normalize numerical data
        numerical_data = scaler.fit_transform(numerical_data)

        # Compute and store vectors
        for stock, numerical_features in zip(stocks, numerical_data):
            # Text-based features (sector, name, and categories)
            sector_embedding = model.encode(stock.sector or "Unknown")
            name_embedding = model.encode(stock.name)

            # Get categories for the stock
            categories = stock_categories.get(stock.ticker, ["General"])
            category_embeddings = np.mean([model.encode(cat) for cat in categories], axis=0)

            # Combine numerical and categorical embeddings
            stock_vector = np.concatenate([numerical_features, sector_embedding, name_embedding, category_embeddings])

            # Insert into Stock_Vectors table
            vector_entry = Stock_Vectors(stock_id=stock.id, embedding=stock_vector.tolist())
            db.session.add(vector_entry)

        db.session.commit()
        print("Stock vectors computed and stored!")

# Tickers to process
tickers = ["AAPL", "MSFT", "GOOGL", "XOM", "WMT", "TWLO", "SAVE", "CHGG", "NEM", "RUN", "PLUG", "QS", "CRSR", "STAG", "BCRX"]
compute_and_store_vectors(tickers)

# Print stored vectors
with app.app_context():
    vectors = Stock_Vectors.query.all()
    for vector in vectors:
        print(f"Stock ID: {vector.stock_id}, Embedding (first 5 values): {vector.embedding[:5]}")
