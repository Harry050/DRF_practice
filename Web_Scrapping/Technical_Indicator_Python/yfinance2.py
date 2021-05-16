import yfinance as yf
import mplfinance as mpf
import talib as ta
import numpy as np
import pandas as pd
import math
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
from datetime import datetime, time
import datetime as dt
from datetime import timezone
import ADX_Indicator as adx_value


def signal_time(data, adx_data_value):
    buy_signals = [np.nan]
    sell_signals = [np.nan]
    signals = []
    last_signal = None


    for i in range(1, len(data)):
        t1= data.index[i].replace(tzinfo=None)
        dt_time = t1.strftime("%H:%M:%S")
        
        if dt_time >= "09:15:00" and dt_time <= "15:30:00":
            #if data['macd_hist'][i-1] < 0 and data['macd_hist'][i] > 0: # without ADX indicator
            if data['macd_hist'][i-1] < 0 and data['macd_hist'][i] > 0 and adx_data_value['ADX'][i] >= 20 and data['rsi'][i] >= 40:
                price = (data['Open'][i] + data['Close'][i]) / 2
                buy_signals.append(price)
                last_signal = 'buy'
                signals.append({
                    'date': data.index[i],
                    'action': 'buy',
                    'price': price,
                    'macd_value': data['macd'][i],
                    'rsi_value': data['rsi'][i],
                    'ticker_name': data['strip_name'][i],
                    'adx_value': adx_data_value['ADX'][i],
                    })
                sell_signals.append(np.nan)
            #elif (data['macd_hist'][i-1] > 0 and data['macd_hist'][i] < 0 and last_signal == 'buy'):
            elif (data['macd_hist'][i-1] > 0 and data['macd_hist'][i] < 0 and last_signal == 'buy') or (last_signal == 'buy' and ((data['Open'][i] + data['Close'][i]) / 2) + ((((data['Open'][i] + data['Close'][i]) / 2) * 0.80)/100)):
                price = (data['Open'][i] + data['Close'][i]) / 2
                #print("This is the selling price" + str(price)  + "This is the price buy after increase " + str(((data['Open'][i] + data['Close'][i]) / 2) + ((((data['Open'][i] + data['Close'][i]) / 2) * 0.25)/100)))
                sell_signals.append(price)
                last_signal = 'sell'
                signals.append({
                    'date': data.index[i],
                    'action': 'sell',
                    'price': price
                    })
                buy_signals.append(np.nan)
            else:
                buy_signals.append(np.nan)
                sell_signals.append(np.nan)

    return buy_signals, sell_signals, signals


def print_performance_summary(signals):
    """Print buy/sell transactions and statistics
    
    Args:
      signals: recorded buy/sell transactions
    """
    pairs = zip(*[iter(signals)]*2)
    rows = []

    profit_count = 0
    profit_pct_avg = 0

    for (buy, sell) in pairs:
        profit = sell['price'] - buy['price']
        profit_pct = profit / buy['price']

        if profit > 0:
            profit_count += 1
        profit_pct_avg += profit_pct

        row = {
            'buy_date': buy['date'],
            'buy_price': buy['price'],
            'sell_price': sell['price'],
            #'duration':  (sell['date'] - buy['date']).days,
            'profit': profit,
            'profit_pct': "{0:.2%}".format(profit_pct),
            'profit_amount': profit*250,
            'macd_value': buy['macd_value'],
            'rsi_value': buy['rsi_value'],
            'ticker_name': buy['ticker_name'],
            'adx_value': buy['adx_value'],
        }
        rows.append(row)
    df_concat = []
    df =  pd.DataFrame(rows, columns=['buy_date', 'duration', 'profit', 'profit_pct', 'profit_amount','buy_price','sell_price', 'macd_value','rsi_value', 'ticker_name', 'adx_value'])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df_concat.append(df)
        #print(df)

    #print(df_concat)

    total_transaction = math.floor(len(signals) / 2)
    stats = {
        'total_transaction': total_transaction,
        'profit_rate': "{0:.2%}".format(profit_count / total_transaction),
        'avg_profit_per_transaction': "{0:.2%}".format(profit_pct_avg / total_transaction)
    }
    for key, value in stats.items():
        print('{0:30}  {1}'.format(key, value))


def download_data():
    plt.style.use('bmh')
    ticker_name = ['ESTER.NS', 'EASEMYTRIP.NS', 'BEPL.NS']
    df_list = list()
    for code in ticker_name:
        data = yf.download(tickers = code, period = "30d", interval = "15m",  group_by = 'ticker', auto_adjust = True,  prepost = True, threads = True, proxy = None)
        data['ticker'] = code
        df_list.append(data)
        df = pd.concat(df_list)
        df.to_csv('Stock Market Data between 100 and 200.csv')


def read_data():
    #ticker_code = ['BEPL.csv', 'EMT.csv', 'Ester.csv']
    ticker_code = ['BajFinance.csv', 'Infy.csv', 'Reliance.csv', 'SBIN.csv', 'SunPharma.csv', 'Titan.csv']

    for code in ticker_code:
        ticker_name = code
        data = pd.read_csv(code)# max, 1y, 3mo

        data.set_index(['Datetime'], inplace=True)
        data.index = pd.to_datetime(data.index)
        data.index.name = 'Date'

        # macd
        data["macd"], data["macd_signal"], data["macd_hist"] = ta.MACD(data['Close'])
        data["rsi"] = ta.RSI(data["Close"])
        data["strip_name"] = data["ticker"]
        
        adx_data = adx_value.adx_indicator_call(code)
        # plot macd

        macd_plot = mpf.make_addplot(data["macd"], panel=1, color='fuchsia', title="MACD")
        rsi_plot = mpf.make_addplot(ta.RSI(data["Close"]),panel=2, color='fuchsia', title="RSI")
        

        colors = ['g' if v >= 0 else 'r' for v in data["macd_hist"]]
        macd_hist_plot = mpf.make_addplot(data["macd_hist"], type='bar', panel=1, color=colors) # color='dimgray'
        macd_signal_plot = mpf.make_addplot(data["macd_signal"], panel=1, color='b')

        # buy/sell
        buy_signals, sell_signals, signals = signal_time(data, adx_data)

        # plot buy/sell
        buy_plot = mpf.make_addplot(buy_signals, alpha=1, type='scatter', marker='^', markersize=50, panel=0)
        sell_plot = mpf.make_addplot(sell_signals, type='scatter', marker='v', markersize=50, panel=0)
        # print buy/sell transaction and statshkhl
        print_performance_summary(signals)

        # plot candle chart and all
        plots = [macd_plot, macd_signal_plot, macd_hist_plot, buy_plot, sell_plot, rsi_plot]
        #mpf.plot(data,type='line', style='yahoo', addplot=plots, title=f"\n{ticker_name}", ylabel='')


#download_data()
read_data()
