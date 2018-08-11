import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.mlab as mlab
import matplotlib.dates as mdates
import pandas as pd
import csv
import numpy as np

def graphData(stock):
	style.use('ggplot')

	df = pd.read_csv(stock, parse_dates=True, index_col=0)

	df_ohlc = df['Closing Price'].resample('10D').ohlc()
	#df_volume = df['Traded Shares'].resample('10D').sum()

	df_ohlc.reset_index(inplace=True)
	df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
	df_ema12 = df['ema_12']
	df_ema26 = df['ema_26']
	Label1 = 'ema_12'
	Label2 = 'ema_26'

	ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)


	ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
	ax1.plot(df_ema26, label= Label2)
	ax1.plot(df_ema12, label= Label1)
	
	ax1.xaxis_date()
	


	candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='y')
	#ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
	ax2.plot(df['macd_12_26_9'],"#5998ff",label='MACD')
	ax2.plot(df['signal_12_26_9'],label='Signal')
	ax2.fill_between(df.index, df['hist_12_26_9'], color = 'gray', alpha=0.5, label='MACD Histogram')
	#ax2.hist(df['hist_12_26_9'],bins=50, color='lightblue',label='histogram')
	#ax2.xaxis.set_major_locator(mdates.YearLocator())
	#ax2.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
	#ax2.xaxis_date()


	plt.xlabel('Date')
	#ax2.set_ylabel('Volume')
	ax1.set_title('Chilime Hydropower')
	#ax1.set_ylabel('Price')
	ax1.legend(loc='upper right')
	ax2.legend(loc='upper right')
	plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
	plt.show()

#while True:
	#stock = input('Stock to plot: ')
graphData('CHCL1.csv')

