#Developing a Pairs Trading strategy for the Indian Banking sector
#If the stock price of A moves in a certain direction, then the stock price of B is expected to make a similar move
#Part of Capstone Project - for MOOC on Advanced Trading Algorithms, ISB on Coursera

#******************************************************************

import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas.io.data as web
import sys

def create_pairs_dataframe(datadir, symbols):
    print "Importing CSV data"   #Open the individual CSV files and read into pandas
    sym1 = web.DataReader(symbols[0], data_source='yahoo',start ='2015/6/1',end=time.strftime("%Y/%m/%d"))
    sym2 = web.DataReader(symbols[1], data_source='yahoo',start ='2015/6/1',end=time.strftime("%Y/%m/%d"))
    #Fetching data form Yahoo Finance for scrips AXISBANK and ICICIBANK

    print "Constructing dual matrix for %s and %s" % symbols
    pairs = pd.DataFrame(index=sym1.index)
    pairs['%s_close' % symbols[0]] = sym1['Adj Close']
    pairs['%s_close' % symbols[1]] = sym2['Adj Close']
    pairs = pairs.dropna()
    return pairs

def check_cointegration(pairs, symbols):
    print "Computing Cointegration"
    coin_result=ts.coint(pairs['%s_close' % symbols[0]],pairs['%s_close' % symbols[1]])   #Cointegration calculating
    return coin_result[1]

def calculate_spread_zscore(pairs, symbols):

    pairs['returns']=np.log(pairs['%s_close' % symbols[0]]/pairs['%s_close' %symbols[1]])
    pairs['mean']=pairs['returns'].rolling(window=30,center=False).mean()
    pairs = pairs.dropna()

    print "Creating the spread/zscore columns"

    pairs['zscore'] = (pairs['returns'] - pairs['mean'])/pairs['returns'].rolling(window=30,center=False).std()

    pairs['returns'].rolling(window=30,center=False).std()
    return pairs

def signal_generate(pairs, symbols,
                    z_entry_threshold=2.0,   #z_enter_threshold for entering a position
                    z_exit_threshold1=0.5,
                    z_exit_threshold2=3.5):   #z_exit_threshold for exiting a position

    pairs['longs'] = (pairs['zscore'] <= -z_entry_threshold)*1.0   #Long or short decision
    pairs['shorts'] = (pairs['zscore'] >= z_entry_threshold)*1.0

    pairs['exits'] = ((np.abs(pairs['zscore']) <= z_exit_threshold1 ) )*1.0

    pairs['long_market'] = 0.0
    pairs['short_market'] = 0.0

    long_market = 0
    short_market = 0

    print "Calculating when to be in the market (long and short)"
    for i, b in enumerate(pairs.iterrows()):
        if pairs['longs'][i-1] == 1.0:   #Compute long positions
            long_market = 1
        if pairs['shorts'][i-1] == 1.0:   #Compute short positions
            short_market = 1

        p.abs(pairs['zscore'][i-1])):
        if pairs['exits'][i-1] == 1.0 or  ((np.abs(pairs['zscore'][i]-pairs['zscore'][i-1]) > 1) and (np.abs(pairs['zscore'][i]+pairs['zscore'][i-1]) < 1)) :
            pairs['exits'][i-1]=1
            long_market = 0
            short_market = 0

        pairs.ix[i]['long_market'] = long_market
        pairs.ix[i]['short_market'] = short_market
    return pairs

def portfolio_returns(pairs, symbols,lot_size):   #Vectorized treatment
    sym1 = symbols[0]
    sym2 = symbols[1]

    pairs['ret_%s' % symbols[0]]=100*((pairs['%s_close' %sym1]/pairs['%s_close' %sym1].shift(1))-1)
    pairs['ret_%s' % symbols[1]]=100*((pairs['%s_close' %sym2]/pairs['%s_close' %sym2].shift(1))-1)

    print "Constructing a portfolio"
    portfolio = pd.DataFrame(index=pairs.index)
    portfolio['positions'] = pairs['long_market'] - pairs['short_market']
    pairs['positions'] = pairs['long_market'] - pairs['short_market']

    pairs[sym1] = pairs['ret_%s' % symbols[0]] * portfolio['positions']
    pairs[sym2] = -1.0*pairs['ret_%s' % symbols[1]] * portfolio['positions']

    pairs['total'] = pairs[sym1] + pairs[sym2]

    portfolio['total'] = pairs[sym1] + pairs[sym2]

    print "Constructing the equity curve"
    portfolio['returns'] = portfolio['total'].pct_change()   #Density curve calculation
    portfolio['returns'].fillna(0.0, inplace=True)
    portfolio['returns'].replace([np.inf, -np.inf], 0.0, inplace=True)
    portfolio['returns'].replace(-1.0, 0.0, inplace=True)

    portfolio['cumu_sum']=portfolio['total'].cumu_sum().plot()
    (100*np.log(pairs['%s_close' % symbols[0]]/ pairs['%s_close' % symbols[0]].shift(1))).cumu_sum().plot()
    (100*np.log(pairs['%s_close' % symbols[1]]/ pairs['%s_close' % symbols[1]].shift(1))).cumu_sum().plot()
    plt.xlabel("Date and time")
    plt.ylabel("Cumulative Returns in %");
    plt.grid(True)

    return portfolio

datadir="H:\QuantPairsTrading\EquityDetails"

if __name__ == "__main__":

    datadir = "H:\QuantPairsTrading\EquityDetails"
    symbols = ('AXIS.NS', 'ICICIBANK.NS')
    lot_size= (2500,400)
    returns = []

    pairs = create_pairs_dataframe(datadir, symbols)
    coint_check = check_cointegration(pairs, symbols)
    if coint_check < 0.47:
         print "Pairs are cointegrated"
         print coint_check

         pairs = calculate_spread_zscore(pairs, symbols)
         pairs = signal_generate(pairs, symbols,
                                 z_entry_threshold=2.0,
                                 z_exit_threshold1=0.5,
                                 z_exit_threshold2=3.5)   #Create the signal spread and then a z-score of the spread

         portfolio = portfolio_returns(pairs, symbols,lot_size)
         pairs.to_csv("H:\QuantPairsTrading\EquityDetails\op.csv")

    else:
         print coint_check
         print "Pairs are not cointegrated. Failed order"
sys.exit(0)
