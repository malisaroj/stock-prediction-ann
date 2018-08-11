import pandas as pd
import numpy as np

df = pd.read_csv('./CHCL1.csv')
# ratio=int(len(df.index)*0.7)

# Generate buy/sell/hold signal using RSI


def signal(df):
    Signal = []
    #price_slow_ema = df['ema_26']     #slowEMA=26   # Your signal line
    #price_fast_ema   = df['ema_12']      #fastEMA=12    The MACD that need to cross the signal line
    #                                              to give you a Buy/Sell signal
    #listLongShort = ["No data"]    # Since you need at least two days in the for loop
    signal = df['signal_12_26_9']     
    macd   = df['macd_12_26_9'] 
    for i in range(len(df.index)):
        if (i < 26):
            Signal.append('Nan')
        else:
         

            if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1]:
                Signal.append("BUY")
                #                          # The other way around
            elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1]:
                Signal.append("SELL")
                #                          # Do nothing if not crossed
            else:
                Signal.append("HOLD")
    return Signal


def updown(df):
    Updown = []
    for i in range(len(df.index)):
        if (i < 1):
            Updown.append('Nan')
        else:
            if (df.iloc[i]['Closing Price'] > df.iloc[i - 1]['Closing Price']):
                Updown.append('Up')
            elif (df.iloc[i]['Closing Price'] < df.iloc[i - 1]['Closing Price']):
                Updown.append('Down')
            else:
                Updown.append('Level')
    return Updown


Updown = updown(df)
Signal = signal(df)
df['Signal'] = Signal
df['Updown'] = Updown
print(df['Signal'])

# df.to_csv('NABIL.csv') 
