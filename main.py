import pytz
import requests
import threading
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime



#function to get sp500 ticker list

def get_sp500_tickers():                                 
    res = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = BeautifulSoup(res.content,'html')
    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))
    tickers = list(df[0].Symbol)
    return tickers

# function to get historic data of tickers using yahoo finance

def get_history(ticker, period_start, period_end, granularity="1d"): 
    import yfinance
    df = yfinance.Ticker(ticker).history(
        start=period_start, 
        end=period_end, 
        interval=granularity, 
        auto_adjust=True
    ).reset_index()

    df = df.rename(columns={
        "Date":"datetime",
        "Open":"open",
        "High":"high",
        "Low":"low",
        "Close":"close",
        "Volume":"volume",
    })

    if df.empty:
        return pd.DataFrame()
    
    df["datetime"] = df["datetime"].dt.tz_convert('UTC')
    df = df.drop(columns=["Dividends", "Stock Splits"])
    df = df.set_index("datetime", drop=True)
    return df

def get_histories(tickers, period_starts, period_ends, granularity="1d"):
    dfs = [None]*len(tickers)
    def _helper(i):
        print(tickers[i])
        df = get_history(
            tickers[i], 
            period_starts[i], 
            period_ends[i], 
            granularity=granularity
        )

        dfs[i] = df

    # Multithreading 

    threads = [threading.Thread(target=_helper, args=(i,)) for i in range(len(tickers))]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    tickers = [tickers[i] for i in range(len(tickers)) if not dfs[i].empty]
    dfs = [df for df in dfs if not df.empty]
    return tickers, dfs

# Function to get tickers data and save it in their particular order 
def get_ticker_dfs(start, end):
    tickers = get_sp500_tickers()
    starts=[start]*len(tickers)
    ends=[end]*len(tickers)

    tickers,dfs = get_histories(tickers, starts, ends, granularity="1d")
    return tickers, {ticker:df for ticker, df in zip(tickers, dfs)}

# tzinfo to localize time to current time zone

period_start = datetime(2010,1,1, tzinfo=pytz.UTC)
period_end = datetime(2020,1,1, tzinfo=pytz.UTC)
tickers, ticker_dfs = get_ticker_dfs(start=period_start, end=period_end)
print(ticker_dfs)