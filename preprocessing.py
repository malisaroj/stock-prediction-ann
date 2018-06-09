import pandas as pd
import numpy as np
import os
import glob
import csv
#import shutil
from technicalindicators import SMA, EMA, MACD, RSI, movingaverage


def cleancsv(source):
    try:
        df = pd.read_csv(source, parse_dates=True)
        print('ok')
    except (FileNotFoundError, IOError):
        print('Wrong file or file path.')
        return
    if df.empty:
        print('df empty')
        return

    # shutil.copyfile(source, destination + source)
    # print('ok')

    df = df.drop_duplicates(subset='Date', keep='first')
    df = df.set_index(pd.DatetimeIndex(df['Date']))

    #df.set_index('Date', drop=False, inplace=True)

    idx = pd.date_range(df.index.min(), df.index.max())

    indexed_data = df.reindex(index=idx, fill_value=np.nan)

    indexed_data = indexed_data.replace('0', np.nan)
    indexed_data = indexed_data.fillna(method='ffill')
    indexed_data = indexed_data.drop('Date', 1)

    print(indexed_data)
    indexed_data.to_csv(source, index_label='Date')
    print('job done')

    # #filename = destination + '/' + source
    # with open(destination, 'w') as f:
    #     indexed_data.to_csv(f, index_label='Date')


def calcopening(source):
    try:
        df = pd.read_csv(source, index_col=0, parse_dates=True)
    except (FileNotFoundError, IOError):
        print('Wrong file or file path.')
        return
    if df.empty:
        return

    df['Opening Price'] = df['Closing Price'].shift(1)
    # The Opening Price must be adjusted so that it is smaller than Maximum Price
    # and larger than Minimum Price
    df['Maximum Price'] = df[['Opening Price', 'Maximum Price', 'Minimum Price', 'Closing Price']].max(axis=1)
    df['Minimum Price'] = df[['Opening Price', 'Maximum Price', 'Minimum Price', 'Closing Price']].min(axis=1)
    df.set_value(df.index[0], 'Opening Price', df.get_value(df.index[0], 'Closing Price'))
    df.to_csv(source, index=True)
    print('complete')


def cleanall(source, destination):

    os.chdir(source)
    for file in glob.glob("*.csv"):
        filename = os.path.basename(file)
        print('Cleaning ' + filename + '...\n')
        cleancsv(filename)


def addtechnicalindicators(source):
    try:
        df = pd.read_csv(source, index_col=0, parse_dates=True)
    except (FileNotFoundError, IOError):
        print('Wrong file or file path.')
        return
    if df.empty:
        return
    df = SMA(df)
    df = EMA(df)
    df = MACD(df)
    df = RSI(df)
    df = movingaverage(df)

    df = df.round(5)
    df.to_csv(source, index=True)


def applyfunc(func, source, *args, **kwargs):
    # os.chdir(source)
    for file in glob.glob("*.csv"):
        filename = os.path.basename(file)
        func(file, *args, **kwargs)


if __name__ == "__main__":
    cleanall('./data/', './data/')

    applyfunc(calcopening, './data/')

    applyfunc(addtechnicalindicators, './data/')
