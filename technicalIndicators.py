import pandas as pd
import numpy as np


def SMA(df, base='Closing Price', target='SMA', period=14):
    """
    Function to compute Simple Moving Average (SMA)

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the SMA needs to be computed from
        target : String indicates the column name to which the computed data needs to be stored
        period : Integer indicates the period of computation in terms of number of candles

    Returns :
        df : Pandas DataFrame with new column added with name 'target'
    """

    df[target] = df[base].rolling(window=period).mean()
    df[target].fillna(0, inplace=True)

    return df


def EMA(df, base='Closing Price', target='EMA', period=14, alpha=False):
    """
    Function to compute Exponential Moving Average (EMA)

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the EMA needs to be computed from
        target : String indicates the column name to which the computed data needs to be stored
        period : Integer indicates the period of computation in terms of number of candles
        alpha : Boolean if True indicates to use the formula for computing EMA using alpha (default is False)

    Returns :
        df : Pandas DataFrame with new column added with name 'target'
    """

    con = pd.concat([df[:period][base].rolling(window=period).mean(), df[period:][base]])

    if (alpha == True):
        # (1 - alpha) * previous_val + alpha * current_val where alpha = 1 / period
        df[target] = con.ewm(alpha=1 / period, adjust=False).mean()
    else:
        # ((current_val - previous_val) * coeff) + previous_val where coeff = 2 / (period + 1)
        df[target] = con.ewm(span=period, adjust=False).mean()

    df[target].fillna(0, inplace=True)
    return df


def MACD(df, fastEMA=12, slowEMA=26, signal=9, base='Closing Price'):
    """
    Function to compute Moving Average Convergence Divergence (MACD)

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        fastEMA : Integer indicates faster EMA
        slowEMA : Integer indicates slower EMA
        signal : Integer indicates the signal generator for MACD
        base : String indicating the column name from which the MACD needs to be computed from (Default Close)

    Returns :
        df : Pandas DataFrame with new columns added for
            Fast EMA (ema_$fastEMA)
            Slow EMA (ema_$slowEMA)
            MACD (macd_$fastEMA_$slowEMA_$signal)
            MACD Signal (signal_$fastEMA_$slowEMA_$signal)
            MACD Histogram (MACD (hist_$fastEMA_$slowEMA_$signal))
    """

    fE = "ema_" + str(fastEMA)
    sE = "ema_" + str(slowEMA)
    macd = "macd_" + str(fastEMA) + "_" + str(slowEMA) + "_" + str(signal)
    sig = "signal_" + str(fastEMA) + "_" + str(slowEMA) + "_" + str(signal)
    hist = "hist_" + str(fastEMA) + "_" + str(slowEMA) + "_" + str(signal)

    # Compute fast and slow EMA
    EMA(df, base, fE, fastEMA)
    EMA(df, base, sE, slowEMA)

    # Compute MACD
    df[macd] = np.where(np.logical_and(np.logical_not(df[fE] == 0), np.logical_not(df[sE] == 0)), df[fE] - df[sE], 0)

    # Compute MACD Signal
    EMA(df, macd, sig, signal)

    # Compute MACD Histogram
    df[hist] = np.where(np.logical_and(np.logical_not(df[macd] == 0), np.logical_not(df[sig] == 0)), df[macd] - df[sig], 0)

    return df


def RSI(df, base='Closing Price', period=21):
    """
    Function to compute Relative Strength Index (RSI)

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the MACD needs to be computed from (Default Close)
        period : Integer indicates the period of computation in terms of number of candles

    Returns :
        df : Pandas DataFrame with new columns added for
            Relative Strength Index (RSI_$period)
    """

    delta = df[base].diff()
    up, down = delta.copy(), delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    rUp = up.ewm(com=period - 1, adjust=False).mean()
    rDown = down.ewm(com=period - 1, adjust=False).mean().abs()

    df['RSI_' + str(period)] = 100 - 100 / (1 + rUp / rDown)
    df['RSI_' + str(period)].fillna(0, inplace=True)

    return df


def movingaverage(df, window_length=14):
    # Get only closing price
    close = df['Closing Price']

    ewma = close.ewm(span=window_length).mean().rename('CP_EMA')
    sma = close.ewm(span=window_length).mean().rename('CP_SMA')

    df = pd.concat([df, ewma, sma], axis=1)
    return df
