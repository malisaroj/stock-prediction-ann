#!/usr/bin/python


import math
import numpy as np
import scipy
from scipy import optimize
import datetime
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt


def fit_fundamental_analysis(time, prices):
    """ Fundamental analysis found at http://es.wikipedia.org/wiki/An%C3%A1lisis_fundamental """

    # Target function
    def fitfunc(p, x): return p[0] + p[1] * np.cos(p[2] * x + p[3])
    # Distance to the target function

    def errfunc(p, x, y): return fitfunc(p, x) - y

    # Initial guess for the parameters
    p0 = [prices[0], 1.0, 1.0, 0.0]

    t = np.array(time)
    p = np.array(prices)

    p1, success = optimize.leastsq(errfunc, p0, args=(t, p))

    print(p1)

    # plt.plot(time, prices)
    plt.plot(fitfunc(p1, t))
    plt.show()

    return p1


os.chdir('./data')

df = pd.read_csv('HBL.csv', parse_dates=True)


df['Closing Price'] = [float(i) for i in df['Closing Price']]
price = df['Closing Price'][::-1]
dates = df['Date'][::-1]


price_ema_slow = df['ema_26']
price_ema_fast = df['ema_12']

# Simulation
account = 5000.0
n_stocks = 0
value = 0.0
stop_loss = 1.0  # Percentual

# Does not seem too optimistic. Possible ways to overcome the limitations:
# 1.- Add a "MOMENTUM" indicator based on the first derivative analysis
# 2.- Add Resistance and Support check
#
# Other things to implement
# 1.- Sector based trading.
n_sessions = len(price)

operations_dates = []
operations = []
dt = []

start_date = datetime.datetime.strptime(dates[1], "%Y-%m-%d")


plt.plot(price_ema_slow)
plt.plot(price_ema_fast)
plt.draw()
for i in range(n_sessions):

    if i == 0.0:
        continue

    time_to_buy = ((price_ema_fast[i] >= price_ema_slow[i]) and
                   (price_ema_fast[i - 1] < price_ema_slow[i - 1]))
    time_to_sell = ((price_ema_fast[i] <= price_ema_slow[i]) and
                    (price_ema_fast[i - 1] > price_ema_slow[i - 1]))

    date = datetime.datetime.strptime(dates[i], "%Y-%m-%d")
    dt.append((date - start_date).days)
    print(date)

    # Check stop loss condition

    if n_stocks > 0:
        stop_loss_price = (1.0 - stop_loss / 100.0) * purchase_price
        is_stop_loss = (price[i] < stop_loss_price)
        print(date, price[i], purchase_price, stop_loss_price, is_stop_loss)
        time_to_sell = time_to_sell or is_stop_loss
    if time_to_buy:
        n_stocks = math.floor(account / price[i])
        value = n_stocks * price[i]
        purchase_price = price[i]
        account = account - value

    if time_to_sell and n_stocks > 0:
        account = account + n_stocks * price[i]
        n_stocks = 0
        operations_dates.append(date)
        a = operations.append(account)

print("The account value is {}".format(account))
print(len(dt), len(price[1:]))

print(fit_fundamental_analysis(dt, price[1:]))
plt.plot(dt, price[1:])
# plt.plot(operations_dates, operations, 'k.-')
plt.show()
