import lzma
import dill as pickle
from datetime import timedelta

def load_pickle(path):
    with lzma.open(path,"rb") as fp:
        file = pickle.load(fp)
    return file


def save_pickle(path,obj):
    with lzma.open(path,"wb") as fp:
        pickle.dump(obj, fp) 

import pandas as pd
import numpy as np

class Alpha():

    def __init__(self, insts, dfs, start , end):
        self.insts = insts
        self.dfs = dfs
        self.start = start
        self.end = end

    def init_portfolio_settings(self, trade_range):
        portfolio_df = pd.DataFrame(index=trade_range)\
            .reset_index()\
            .rename(columns={"index":"datetime"})
        portfolio_df.loc[0,"Capital"] = 10000
        return portfolio_df

    def compute_meta_info(self,trade_range):
        for inst in self.insts:
            df=pd.DataFrame(index=trade_range)
            self.dfs[inst] = df.join(self.dfs[inst]).fillna(method="ffill").fillna(method="bfill")
            self.dfs[inst]["ret"] = -1 + self.dfs[inst]["close"]/self.dfs[inst]["close"].shift(1)
            sampled = self.dfs[inst]["close"] != self.dfs[inst]["close"].shift(1).fillna(method="bfill")
            eligible = sampled.rolling(5).apply(lambda x: int(np.any(x))).fillna(0)
            self.dfs[inst]["eligible"] =eligible.astype(int) & (self.dfs[inst]["close"] > 0).astype(int)
            input(self.dfs[inst])
        return

    
    def run_simulation(self):
        print("Running backtest")
        start = self.start + timedelta(hours=5)
        end = self.end + timedelta(hours=5)
        date_range = pd.date_range(start, end, freq="D")
        self.compute_meta_info(trade_range=date_range)
        portfolio_df = self.init_portfolio_settings(trade_range=date_range)
        for i in portfolio_df.index:
            date = portfolio_df.loc[i, "datetime"]

            if i != 0:
                #compute pnl
                pass

            alpha_scores = {}
            #compute alpha signals

            #compute positions and other info
