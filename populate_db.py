import yfinance as yf
from app import create_app, db
from models import Stock

# Initialize your Flask app
app = create_app()

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

def fetch_and_populate_stocks(tickers):
    with app.app_context():  # Ensure an app context is active
        for ticker in tickers:
            stock_info = yf.Ticker(ticker).info

            # Fetch categories for the stock
            categories = stock_categories.get(ticker, ["General"])

            # Populate the stock
            stock = Stock(
                ticker=ticker,
                name=stock_info.get("shortName", ticker),
                sector=stock_info.get("sector", "Unknown"),
                market_cap=stock_info.get("marketCap", None),
                categories=categories  # Add categories here
            )
            db.session.add(stock)
        db.session.commit()
        print("Stocks added to the database.")

tickers = ["AAPL", "MSFT", "GOOGL", "XOM", "WMT", "TWLO", "SAVE", "CHGG", "NEM", "RUN", "PLUG", "QS", "CRSR", "STAG", "BCRX"]
fetch_and_populate_stocks(tickers)
