# INF601 - Advanced Programming in Python
# Fernando Duffoo
# Mini Project 1


import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# (5/5 points) Initial comments with your name, class and project at the top of your .py file.
# (5/5 points) Proper import of packages used.
# (20/20 points) Using an API of your choice (yfinance works), collect the closing price of 5 of your favorite stock tickers for the last 10 trading days.
# (10/10 points) Store this information in a list that you will convert to a array in NumPy.
# (10/10 points) Plot these 5 graphs. Feel free to add as much information to the graphs as you like exploring the documentation for matplotlib. At minimum it just needs to show 10 data points.
# (10/10 points) Save these graphs in a folder called charts as PNG files. Do not upload these to your project folder, the project should save these when it executes. You may want to add this folder to your .gitignore file.
# (10/10 points) There should be a minimum of 5 commits on your project, be sure to commit often!
# (10/10 points) I will be checking out the main branch of your project. Please be sure to include a requirements.txt file which contains all the packages that need installed. You can create this fille with the output of pip freeze at the terminal prompt.
# (20/20 points) There should be a README.md file in your project that explains what your project is, how to install the pip requirements, and how to execute the program. Please use the GitHub flavor of Markdown.

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

