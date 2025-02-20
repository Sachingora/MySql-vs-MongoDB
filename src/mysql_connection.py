import mysql.connector
import pandas as pd

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root",  # Replace with your MySQL root password
    database="stock_analysis"
)
cursor = connection.cursor()
print("Connected to MySQL!")

# ------------------ Load and Upload Tweets Dataset ------------------

# Load the tweets dataset
tweets = pd.read_csv(r'C:\Users\Sachin Gora\OneDrive\Desktop\project\data\stocktweet.csv')

# Convert 'date' column to MySQL-compatible format
tweets['date'] = pd.to_datetime(tweets['date'], dayfirst=True).dt.strftime('%Y-%m-%d')

# Bulk insert tweets into MySQL
tweets_values = tweets.values.tolist()  # Convert DataFrame to a list of lists
cursor.executemany(
    "INSERT IGNORE INTO tweets (id, date, ticker, tweet) VALUES (%s, %s, %s, %s)",
    tweets_values
)

# Commit changes for tweets data
connection.commit()
print(f"Tweets dataset uploaded successfully. Rows inserted: {cursor.rowcount}")

# ------------------ Load and Upload Stock Prices Dataset ------------------

# Load the stock prices dataset
stock_prices = pd.read_csv(r'C:\Users\Sachin Gora\OneDrive\Desktop\project\data\AAPL.csv')

# Convert 'Date' column to MySQL-compatible format
stock_prices['Date'] = pd.to_datetime(stock_prices['Date']).dt.strftime('%Y-%m-%d')

# Add a 'ticker' column to the dataset (e.g., 'AAPL')
stock_prices['ticker'] = 'AAPL'

# Rearrange columns to match MySQL table structure
stock_prices = stock_prices[['Date', 'ticker', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

# Bulk insert stock prices into MySQL
stock_prices_values = stock_prices.values.tolist()  # Convert DataFrame to a list of lists
cursor.executemany(
    """
    INSERT IGNORE INTO stock_prices (date, ticker, open, high, low, close, adj_close, volume) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """,
    stock_prices_values
)

# Commit changes for stock prices data
connection.commit()
print(f"Stock prices dataset uploaded successfully. Rows inserted: {cursor.rowcount}")

# ------------------ Close Connection ------------------
connection.close()
print("Database connection closed.")
