import pandas as pd
import numpy as np

df = pd.read_csv('./data/NABIL.csv')
# ratio=int(len(df.index)*0.7)

# Generate buy/sell/hold signal using RSI


def signal(df):
    Signal = []
    for i in range(len(df.index)):
        if (i < 16):
            Signal.append('Nan')
        else:
            if (df.iloc[i]['Closing Price'] > df.iloc[i - 1]['Closing Price']) and (float(df.iloc[i]['RSI_21']) > float(df.iloc[i - 1]['RSI_21'])) and (float(df.iloc[i]['RSI_21']) > 50):
                Signal.append('Buy')
            elif (df.iloc[i]['Closing Price'] < df.iloc[i - 1]['Closing Price']) and (float(df.iloc[i]['RSI_21']) < float(df.iloc[i - 1]['RSI_21'])) and (float(df.iloc[i]['RSI_21']) < 50):
                Signal.append('Sell')
            else:
                Signal.append('Hold')
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
