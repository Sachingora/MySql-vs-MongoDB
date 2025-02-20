from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['stock_analysis']
print("Connected to MongoDB!")

# ------------------ Load and Upload Tweets Dataset ------------------

# Load the tweets dataset
tweets = pd.read_csv(r'C:\Users\Sachin Gora\OneDrive\Desktop\project\data\stocktweet.csv')

# Convert 'date' column to MongoDB-compatible format
tweets['date'] = pd.to_datetime(tweets['date'], dayfirst=True).dt.strftime('%Y-%m-%d')

# Convert DataFrame to a list of dictionaries (records)
tweets_docs = tweets.to_dict('records')

# Insert documents into the 'tweets' collection
db.tweets.insert_many(tweets_docs)
print(f"Tweets dataset uploaded successfully. Rows inserted: {len(tweets_docs)}")

# ------------------ Load and Upload Stock Prices Dataset ------------------

# Load the stock prices dataset
stock_prices = pd.read_csv(r'C:\Users\Sachin Gora\OneDrive\Desktop\project\data\AAPL.csv')

# Convert 'Date' column to MongoDB-compatible format
stock_prices['Date'] = pd.to_datetime(stock_prices['Date']).dt.strftime('%Y-%m-%d')

# Add a 'ticker' column to the dataset (e.g., 'AAPL')
stock_prices['ticker'] = 'AAPL'

# Convert DataFrame to a list of dictionaries (records)
stock_prices_docs = stock_prices.to_dict('records')

# Insert documents into the 'stock_prices' collection
db.stock_prices.insert_many(stock_prices_docs)
print(f"Stock prices dataset uploaded successfully. Rows inserted: {len(stock_prices_docs)}")

# ------------------ Close MongoDB Connection ------------------
print("Database operations completed successfully.")
