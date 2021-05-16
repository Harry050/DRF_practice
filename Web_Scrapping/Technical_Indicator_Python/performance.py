import pandas as pd
import math


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
        if buy['action'] == 'short_buy' or buy['action'] == 'short_sell':
            profit = buy['short_price'] - sell['short_price'] 
            profit_pct = profit / buy['short_price']

            if profit > 0:
                profit_count += 1
            profit_pct_avg += profit_pct

            row = {
                'buy_date': buy['date'],
                'buy_price': buy['short_price'],
                'sell_price': sell['short_price'],
                #'duration':  (sell['date'] - buy['date']).days,
                'profit': profit,
                'profit_pct': "{0:.2%}".format(profit_pct),
                'profit_amount': profit*250,
                'ema5': buy['ema5'],
                'ema20': buy['ema20'],
                'ema200': buy['ema200'],
                'buy_type': 'Short Buy',
                'ticker_name': buy['ticker_name'],
                'rsi': buy['rsi'],
            }
            rows.append(row)
        elif buy['action'] == 'pull_buy'  or buy['action'] == 'pull_sell':
            profit = sell['pull_price'] - buy['pull_price'] 
            profit_pct = profit / buy['pull_price']

            if profit > 0:
                profit_count += 1
            profit_pct_avg += profit_pct

            row = {
                'buy_date': buy['date'],
                'buy_price': buy['pull_price'],
                'sell_price': sell['pull_price'],
                #'duration':  (sell['date'] - buy['date']).days,
                'profit': profit,
                'profit_pct': "{0:.2%}".format(profit_pct),
                'profit_amount': profit*250,
                'ema5': buy['ema5'],
                'ema20': buy['ema20'],
                'ema200': buy['ema200'],
                'buy_type': 'Pull Buy',
                'ticker_name': buy['ticker_name'],
                'rsi': buy['rsi'],
            }
            rows.append(row)

    df_concat = []
    df =  pd.DataFrame(rows, columns=['buy_date', 'profit', 'profit_pct', 'profit_amount','buy_price','sell_price', 'ema5', 'ema20', 'ema200', 'buy_type', 'ticker_name', 'rsi'])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df_concat.append(df)
        #print(df)
    #df.to_csv('Ema SBin.csv')
    #print(df_concat)

    total_transaction = math.floor(len(signals) / 2)
    stats = {
        'total_transaction': total_transaction,
        'profit_rate': "{0:.2%}".format(profit_count / total_transaction),
        'avg_profit_per_transaction': "{0:.2%}".format(profit_pct_avg / total_transaction)
    }
    for key, value in stats.items():
        print('{0:30}  {1}'.format(key, value))