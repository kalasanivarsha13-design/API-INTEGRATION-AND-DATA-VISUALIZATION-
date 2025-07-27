import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def fetch_crypto_data(coin_id="bitcoin", currency="usd", days=30):
    """Fetch historical market data from CoinGecko API"""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": currency,
        "days": days,
        "interval": "hourly"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data['prices']

def process_data(prices):
    """Convert price data into a pandas DataFrame"""
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    df.set_index("timestamp", inplace=True)
    df = df.resample('4H').mean()  # Aggregate to 4-hour intervals
    return df

def visualize_data(df, coin_name="Bitcoin"):
    """Plot the price data using Plotly"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["price"],
        mode='lines+markers',
        name=coin_name,
        line=dict(color='royalblue', width=2),
        marker=dict(size=4)
    ))
    fig.update_layout(
        title=f"{coin_name} Price Over Time",
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        template="plotly_dark",
        hovermode="x unified"
    )
    fig.show()

def main():
    print("Fetching data from CoinGecko...")
    prices = fetch_crypto_data("bitcoin", "usd", 30)
    print("Processing data...")
    df = process_data(prices)
    print("Generating visualization...")
    visualize_data(df)

if __name__ == "__main__":
    main()
