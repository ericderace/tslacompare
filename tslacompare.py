# tslacompare.py
# 
# 2024 Eric Hebert
#
# Compare TSLA stock data for a specified number of years including the current year to check for seasonal stock price changes
#
# License: MIT

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import argparse
from matplotlib.dates import DateFormatter

# Setup command-line argument parsing
parser = argparse.ArgumentParser(description='Plot TSLA stock data for a specified number of years including the current year, with customizable theme options.')
parser.add_argument('-y', '--years', type=int, default=2, help='Number of years to plot, including the current year. Default is 2.')
parser.add_argument('--percentage', action='store_true', help='Plot percentage gain/loss compared to the year\'s average closing price.')
parser.add_argument('--light', action='store_true', help='Use a light theme for the plot. Custom dark grey theme is used by default.')
args = parser.parse_args()

# Define the ticker
ticker = 'TSLA'
current_year = pd.to_datetime('today').year

# Set the custom style properties based on the chosen theme
if args.light:
    plt.style.use('default')  # Use Matplotlib's default style for the light theme
else:
    # Custom dark grey theme
    plt.rcParams['figure.facecolor'] = '#2d2d2d'  # Dark grey background for the figure
    plt.rcParams['axes.facecolor'] = '#2d2d2d'  # Dark grey background for the axes
    plt.rcParams['axes.edgecolor'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    plt.rcParams['lines.color'] = 'white'
    plt.rcParams['grid.color'] = 'gray'
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['figure.figsize'] = (14, 7)

# Initialize a figure for plotting
plt.figure()

# Loop through the specified number of years including the current year
for i in range(args.years - 1, -1, -1):
    start_year = current_year - i
    end_year = f'{start_year}-12-31'
    if i == 0:  # For the current year, adjust the end date to today
        end_year = pd.to_datetime('today').strftime('%Y-%m-%d')

    # Fetch the data for the year
    data = yf.download(ticker, start=f'{start_year}-01-01', end=end_year)

    if args.percentage:
        # Calculate the year's average closing price
        yearly_avg = data['Adj Close'].mean()
        
        # Calculate the percentage gain/loss compared to the yearly average
        data['Percentage Change'] = (data['Adj Close'] - yearly_avg) / yearly_avg * 100
        
        # If not the current year, adjust the index to match the current year for plotting
        if i != 0:
            data.index = data.index.map(lambda x: x.replace(year=current_year))

        # Plot the percentage change
        plt.plot(data.index, data['Percentage Change'], label=f'{start_year}')
    else:
        # If not the current year, adjust the index to match the current year for plotting
        if i != 0:
            data.index = data.index.map(lambda x: x.replace(year=current_year))
        
        # Plot the data
        plt.plot(data.index, data['Adj Close'], label=f'{start_year}')

# Format the X-axis to display month abbreviations
plt.gca().xaxis.set_major_formatter(DateFormatter('%b'))

# Adjust the x-axis to cover from January 1 to December 31
plt.xlim([pd.Timestamp(current_year, 1, 1), pd.Timestamp(current_year, 12, 31)])

# Add title, labels, legend, and grid
plot_title = 'Percentage Gain/Loss from annual average price' if args.percentage else 'Adjusted Close Price'
plt.title(f'{ticker} - Comparison of the Last {args.years} Years ({plot_title})')
plt.xlabel('Month')
plt.ylabel(plot_title)
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

# Save the graph as an image
plt.savefig('./tslacompare.png')
