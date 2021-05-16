import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
from datetime import date

""" Pandas """
def candle_stick_chart():
    historic_df = pd.read_csv("Stock Market.csv")

    dates = pd.to_datetime(historic_df['Datetime'], format="%Y-%m-%d %H:%M:%S.%f")
    openp = historic_df['Open']
    highp =  historic_df['High']
    lowp =  historic_df['Low']
    closep =  historic_df['Close']

    """ Matplotlib """
    ax1 = plt.subplot2grid((1,1), (0,0))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    x = 0
    ohlc = []

    while x < len(dates):
        d = mdates.date2num(dates[x])
        append_me = d, openp.values[x], highp.values[x], lowp.values[x], closep.values[x]
        ohlc.append(append_me)
        x += 1

    candlestick_ohlc(ax1, ohlc, width=0.001, colorup='g', colordown='r')
    plt.show()


from datetime import datetime, time

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        print(check_time)
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

# Original test case from OP
is_time_between(time(9,30), time(14,30))

# Test case when range crosses midnight
