import pandas as pd
import plotly.express as px
import streamlit as st

# Load data
try:
    sentiment_data = pd.read_csv('C:/Users/Sachin Gora/OneDrive/Desktop/project/data/sentiment_summary.csv')
    arima_forecast = pd.read_csv('C:/Users/Sachin Gora/OneDrive/Desktop/project/data/arima_forecast.csv')
    lstm_forecast = pd.read_csv('C:/Users/Sachin Gora/OneDrive/Desktop/project/data/lstm_forecast.csv')
except FileNotFoundError as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Rename columns if necessary
if 'Unnamed: 0' in arima_forecast.columns:
    arima_forecast.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
if 'Unnamed: 0' in lstm_forecast.columns:
    lstm_forecast.rename(columns={'Unnamed: 0': 'date'}, inplace=True)

# Validate and ensure the 'date' column exists
if 'date' in arima_forecast.columns:
    arima_forecast['date'] = pd.to_datetime(arima_forecast['date'], errors='coerce')
else:
    st.error("The 'date' column is missing in the ARIMA forecast data.")
    st.stop()

if 'date' in lstm_forecast.columns:
    lstm_forecast['date'] = pd.to_datetime(lstm_forecast['date'], errors='coerce')
else:
    # Adding a dummy date column if it doesn't exist
    st.warning("The 'date' column is missing in the LSTM forecast data. Adding a default 'date' column.")
    lstm_forecast['date'] = pd.date_range(start="2020-01-01", periods=len(lstm_forecast), freq="D")

# Add dummy 'ticker' column if missing
if 'ticker' not in arima_forecast.columns:
    arima_forecast['ticker'] = 'Unknown'
if 'ticker' not in lstm_forecast.columns:
    lstm_forecast['ticker'] = 'Unknown'

# Streamlit layout
st.title("Stock Analysis Dashboard")

# Dropdown for selecting company
if 'ticker' in sentiment_data.columns:
    company = st.selectbox("Select a Company", sentiment_data['ticker'].unique())
else:
    st.error("The 'ticker' column is missing in the sentiment data.")
    st.stop()

# Sentiment trends visualization
if 'date' in sentiment_data.columns:
    filtered_sentiment = sentiment_data[sentiment_data['ticker'] == company]
    sentiment_fig = px.bar(filtered_sentiment, x='date', y='positive', title=f"Sentiment Trends for {company}")
    st.plotly_chart(sentiment_fig)
else:
    st.error("The 'date' column is missing in the sentiment data.")

# ARIMA forecast visualization
if 'date' in arima_forecast.columns and 'predicted_mean' in arima_forecast.columns:
    filtered_arima = arima_forecast[arima_forecast['ticker'] == company]
    arima_fig = px.line(filtered_arima, x='date', y='predicted_mean', title=f"ARIMA Forecast for {company}")
    st.plotly_chart(arima_fig)
else:
    st.error("The required columns are missing in the ARIMA forecast data.")

# LSTM forecast visualization
if 'date' in lstm_forecast.columns and 'predicted_mean' in lstm_forecast.columns:
    filtered_lstm = lstm_forecast[lstm_forecast['ticker'] == company]
    lstm_fig = px.line(filtered_lstm, x='date', y='predicted_mean', title=f"LSTM Forecast for {company}")
    st.plotly_chart(lstm_fig)
else:
    st.error("The required columns are missing in the LSTM forecast data.")


# to run the app, run the following command in the terminal: streamlit run dashboard/app.py
