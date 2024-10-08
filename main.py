import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
import sys
import os
from datetime import datetime
import plotly.graph_objects as go
from flask import Flask, render_template

# Initialize Flask app (for deployment as a web app)
app = Flask(__name__)

# Set up your workspace folders if they don't exist
os.makedirs('charts', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Get user input for date range
start_date = sys.argv[1] if len(sys.argv) > 1 else "2024-01-01"
end_date = sys.argv[2] if len(sys.argv) > 2 else "2024-01-10"

# List of tickers to analyze
tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']

# Initialize an empty list for closing prices
closing_prices_list = []

for ticker in tickers:
    try:
        myticker = yf.Ticker(ticker)
        history = myticker.history(start=start_date, end=end_date)

        if history.empty:
            raise ValueError(f"No data found for {ticker}")

        # Append closing prices to the list
        closing_prices_list.append(list(history['Close']))

        # Save data to CSV file
        history.to_csv(f'data/{ticker}_data.csv')

    except Exception as e:
        print(f"Error retrieving data for {ticker}: {e}")

# Convert the list of lists to a NumPy array
closing_prices_array = np.array(closing_prices_list)

# Plot and save charts with additional features
for i, ticker in enumerate(tickers):
    dates = history.index
    prices = closing_prices_array[i, :]

    # Plot with matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(dates, prices, marker='o', linestyle='-', color='b')
    ax.set_title(f'{ticker} - Closing Prices')
    ax.set_xlabel('Date')
    ax.set_ylabel('Closing Price')
    ax.grid(True)

    # Add moving average
    history['20_MA'] = history['Close'].rolling(window=20).mean()
    ax.plot(dates, history['20_MA'], label='20-Day MA', color='orange')

    # Format dates on the x-axis
    date_format = DateFormatter("%m-%d")
    ax.xaxis.set_major_formatter(date_format)
    plt.xticks(rotation=45)

    # Show price labels on each data point
    for date, price in zip(dates, prices):
        ax.text(date, price, f'{price:.2f}', ha='left', va='bottom')

    # Save the plot
    plt.savefig(f'charts/{ticker}_chart.png')
    plt.show()
    plt.close()

    # Plot with Plotly for interactive visualization
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines+markers', name=ticker))
    fig.update_layout(title=f'{ticker} - Closing Prices', xaxis_title='Date', yaxis_title='Closing Price')
    fig.show()

# Display correlation matrix
correlations = np.corrcoef(closing_prices_array)
print("Correlation Matrix:\n", correlations)

# Flask route for web app (if deploying)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

# Display the closing prices array
print(closing_prices_array)
