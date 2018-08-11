import csv
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import datetime

# -------------------------------------------------------------
# Definition for MACD as follows: 
# MACD Line = 12-day EMA - 26-day EMA
# Signal Line = 9-day EMA of MACD Line
# MACD Histogram = MACD Line - Signal Line
#
# EMA: Exponential Moving Average; various definitions exist
# -------------------------------------------------------------

# returns time_series for macd line
def macd(time_series, slow_period=26, fast_period=12):
    emaslow = time_series.ewm(span=slow_period, adjust=False).mean()
    emafast = time_series.ewm(span=fast_period, adjust=False).mean()    
    return emafast, emaslow, emafast - emaslow

def graphData(stock):
    # Set up parameters for obtaining historical stock prices
    start_date = '2017-01-01'
    end_date = datetime.date.today()
    #ticker = 'SBUX'
    #source = 'google'

    # download historical stock prices
    df = pd.read_csv(stock, parse_dates=True, index_col=0)

    #df = datareader.DataReader(ticker, source, start_date, end_date)

    # set up MACD parameters
    slow_period = 26
    fast_period = 12
    signal_period = 9

    # compute the MACD datapoints
    emaslow, emafast, macd_line = macd(df['Closing Price'], slow_period, fast_period)
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

    # draw the MACD lines and histogram
    f1, ax1 = plt.subplots(figsize = (8,4))
    ax1.plot(df.index, df['Closing Price'], color = 'black', lw=2, label='Close')
    ax1.plot(df.index, emaslow, color ='blue', lw=1, label='EMA(26)')
    ax1.plot(df.index, emafast, color ='red', lw=1, label='EMA(12)')

    f2, ax2 = plt.subplots(figsize = (8,4))
    ax2.plot(df.index, macd_line, color='green', lw=1,label='MACD Line(26,12)')
    ax2.plot(df.index, signal_line, color='purple', lw=1, label='Signal Line(9)')

    # set other parameters
    ax1.legend(loc='upper right')
    ax1.set(title = 'Chilime Hydropower Stock Price', ylabel = 'Price')
    ax2.fill_between(df.index, macd_line - signal_line, color = 'gray', alpha=0.5, label='MACD Histogram')
    ax2.set(title = 'MACD(26,12,9)', ylabel='MACD')
    ax2.legend(loc = 'upper right')
    ax2.grid(False)

    plt.show()

graphData('CHCL1.csv')
