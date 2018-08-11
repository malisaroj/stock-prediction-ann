import numpy as np
import pandas as pd  
import csv
import matplotlib.pyplot as plt
import datetime
from technicalIndicators import RSI, BBand, ADX, MACD

def analyzer(stock):
    df = pd.read_csv(stock, parse_dates=True, index_col=0)
    MACD(df)
    print(df.tail())
    RSI(df)
  
    BBand(df)

    
    



    

	# # Fine-tune figure; make subplots close to each other and hide x ticks for
	# # all but bottom plot.
	# f.subplots_adjust(hspace=0)
	# plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)


    plt.figure()



    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=4, colspan=1)
    
    ax1.set_title('Sharing both axes')

    ax2 = plt.subplot2grid((6,1), (4,0), rowspan=1, colspan=1)
    #ax1.set_title('Sharing both axes')
    ax3 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1)
    
    #ax2.set_title('Sharing both axes')
    #f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
    x_axis = df.index.get_level_values(0)
    plt.xlabel('Date')
    ax1.set_ylabel('')
    ax1.fill_between(x_axis, df['UpperBB_20_2'], df['LowerBB_20_2'], color='grey')
    #ax1.plot(x_axis, df['UpperBB_20_2'], color='black')

	# Plot Adjust Closing Price and Moving Averages
    ax1.plot(x_axis, df['Closing Price'], color='black', lw=1, label='Closing Price')
    ax1.plot(x_axis, df['ema_26'], color='red', lw=2, label='ema_26')

    ax1.set_title('Chilime Hydropower Company Limited')

    ax2.set_ylabel('')
    
    ax2.plot(x_axis, df['RSI_21'],label='RSI', color='purple')
    ax2.set_ylabel('')


    ax3.plot(x_axis,df['macd_12_26_9'],label='MACD', color='brown')



	# plt.xlabel('Date')
	# plt.ylabel('Price')


    ax1.legend(loc = 'upper right')
    ax2.legend(loc = 'upper right')
    ax3.legend(loc = 'upper right')
    plt.subplots_adjust(left=0.11, bottom=0.24, right=0.90, top=0.90, wspace=0.2, hspace=0)
    plt.show()


analyzer('CHCL1.csv')