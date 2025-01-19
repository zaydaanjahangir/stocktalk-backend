import yfinance as yf
from app import create_app, db
from models import Stock

app = create_app()  # Initialize your Flask app

def fetch_and_populate_stocks(tickers):
    with app.app_context():  # Ensure an app context is active
        for ticker in tickers:
            stock_info = yf.Ticker(ticker).info

            stock = Stock(
                ticker=ticker,
                name=stock_info.get("shortName", ticker),
                sector=stock_info.get("sector", "Unknown"),
                market_cap=stock_info.get("marketCap", None),
            )
            db.session.add(stock)
        db.session.commit()
        print("Stocks added to the database.")

tickers = ["AAPL", "MSFT", "GOOGL", "XOM", "WMT", "TWLO", "SAVE", "CHGG", "NEM", "RUN", "PLUG", "QS", "CRSR", "STAG", "BCRX"]
fetch_and_populate_stocks(tickers)
