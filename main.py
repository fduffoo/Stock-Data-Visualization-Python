import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']

# Initialize an empty list
closing_prices_list = []

for ticker in tickers:
    myticker = yf.Ticker(ticker)
    history = myticker.history(start="2024-01-01", end="2024-01-10")

    # Append closing prices to the list
    closing_prices_list.append(list(history['Close']))

# Convert the list of lists to a NumPy array
closing_prices_array = np.array(closing_prices_list)

# Plot and save charts
for i, ticker in enumerate(tickers):
    dates = history.index[-10:]  # Extract the last 10 dates
    prices = closing_prices_array[i, -10:]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(dates, prices, marker='o', linestyle='-', color='b')
    ax.set_title(f'{ticker} - Closing Prices')
    ax.set_xlabel('Date')
    ax.set_ylabel('Closing Price')
    ax.grid(True)

    # Format dates on the x-axis
    date_format = DateFormatter("%m-%d")  # Example: Jan-01
    ax.xaxis.set_major_formatter(date_format)
    plt.xticks(rotation=45)  # Rotate date labels for better visibility

    # Show price labels on each data point
    for date, price in zip(dates, prices):
        ax.text(date, price, f'{price:.2f}', ha='left', va='bottom')

    plt.savefig(f'charts/{ticker}_chart.png')
    plt.show()  # Display the plot
    plt.close()

# Display
print(closing_prices_array)

