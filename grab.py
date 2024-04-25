import yfinance as yf
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import datetime



OPEN = 0
CLOSE = 1
LOW = 2
HIGH = 3


# Periods - “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
# Intervals - 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo



def min_max_normalization(data, min_val=None, max_val=None):
    if min_val is None:
        min_val = min(data)
    if max_val is None:
        max_val = max(data)

    normalized_data = [(x - min_val) / (max_val - min_val) for x in data]
    return normalized_data, min_val, max_val


def make_data(data):
    final_data = {}
    for ticker in data:
        final_data[ticker] = []
        for i in range(90, len(data[ticker])):
            day = []

            avgs = [90, 60, 30, 14, 7, 3, 2]

            for avg in avgs:
                day.append(np.mean([d[CLOSE] for d in data[ticker][i-avg:i]]))  # Last avg periods



            day.append(data[ticker][i-1][CLOSE])  # Last period
            
            day.append(data[ticker][i][OPEN])  # OPEN

            target = (data[ticker][i][CLOSE] / data[ticker][i][OPEN] - 1) * 100
            
            final_data[ticker].append((day, target))
    return final_data


def plot_ticker(data):
    plt.plot([d[-1] for d in data], color='blue', label='OPEN')
    plt.plot([d[0] for d in data], color='red', label='90')
    plt.plot([d[1] for d in data], color='green', label='60')
    plt.plot([d[2] for d in data], color='purple', label='30')
    plt.legend()
    plt.show()



def get_data(ticker, period='1y', interval='1h'):
    ticker_info = yf.Ticker(ticker)

    history = ticker_info.history(period=period, interval=interval)

    X = []

    for i in range(0, len(history)):
        day = history.iloc[i]
        predata = []
        predata.append(day['Open'])  # Open, Close, Low, High, Volume
        predata.append(day['Close'])
        predata.append(day['Low'])
        predata.append(day['High'])
        # predata.append(day['Volume'])

        X.append(predata)
    
    return X

def get_data_date(ticker, end, interval, dif=22):
    ticker_info = yf.Ticker(ticker)

    history = None

    if interval == '1m':
        start_date = datetime.datetime.strptime(end, '%Y-%m-%d').date() - datetime.timedelta(days=7)
    elif interval == '2m':
        start_date = datetime.datetime.strptime(end, '%Y-%m-%d').date() - datetime.timedelta(days=30-dif)
    elif interval == '5m' or interval == '15m' or interval == '30m':
        start_date = datetime.datetime.strptime(end, '%Y-%m-%d').date() - datetime.timedelta(days=60-dif)
    elif interval == '1h':
        start_date = datetime.datetime.strptime(end, '%Y-%m-%d').date() - datetime.timedelta(days=730-dif)
    elif interval == '1d':
        start_date = datetime.datetime.strptime(end, '%Y-%m-%d').date() - datetime.timedelta(days=1500)
    elif interval == '1wk':
        start_date = datetime.datetime.strptime(end, '%Y-%m-%d').date() - datetime.timedelta(days=1500)
    else:
        history = ticker_info.history(end=end, interval=interval, period='max')

    if history is None:
        history = ticker_info.history(start=start_date, end=end, interval=interval)

    history.dropna()

    X = []

    for i in range(0, len(history)):
        day = history.iloc[i]
        predata = []
        t = str(day.name)
        predata.append(day['Open'])  # Open, Close, Low, High, Volume
        predata.append(day['Close'])
        predata.append(day['Low'])
        predata.append(day['High'])
        predata.append(day['Volume'])

        X.append([t[:t.rfind('-')], predata])
    
    return X


# if __name__ == '__main__':
#     top_30_stocks = [
#         "AAPL",  # Apple Inc.
#         "MSFT",  # Microsoft Corporation
#         "AMZN",  # Amazon.com Inc.
#         "GOOGL",  # Alphabet Inc.
#         "META",  # Meta Platforms, Inc.
#         "TSLA",  # Tesla, Inc.
#         "JNJ",  # Johnson & Johnson
#         "JPM",  # JPMorgan Chase & Co.
#         "V",  # Visa Inc.
#         "MA",  # Mastercard Incorporated
#         "WMT",  # Walmart Inc.
#         "PG",  # The Procter & Gamble Company
#         "KO",  # The Coca-Cola Company
#         "PFE",  # Pfizer Inc.
#         "NFLX",  # Netflix, Inc.
#         "NVDA",  # NVIDIA Corporation
#         "HD",  # The Home Depot, Inc.
#         "MCD",  # McDonald's Corporation
#         "ADBE",  # Adobe Inc.
#         "CRM",  # Salesforce.com Inc.
#         "PYPL",  # PayPal Holdings, Inc.
#         "BAC",  # Bank of America Corporation
#         "XOM",  # Exxon Mobil Corporation
#         "T",  # AT&T Inc.
#         "VZ",  # Verizon Communications Inc.
#         "DIS",  # The Walt Disney Company
#         "IBM",  # International Business Machines Corporation
#         "CSCO",  # Cisco Systems, Inc.
#         "CVX"  # Chevron Corporation
#     ]

#     period = '1y'
#     interval = '1h'

#     data = get_data('AAPL', period=period, interval=interval)

#     json.dump(data, open('aapl.json', 'w+'))


if __name__ == '__main__':
    history = get_data_date(ticker='AAPL', end='2024-02-24', interval='2m')

    # 1h 730 days
    # 5m last 60 days
    # 1m last 7 days

    for k in history:
        print(k, history[k])
    print(len(history))









