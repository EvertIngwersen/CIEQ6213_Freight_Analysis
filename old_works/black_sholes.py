# -*- coding: utf-8 -*-
"""
Created on Mon May  5 13:04:06 2025

@author: evert
"""

import yfinance as yf

from scipy.stats import norm
from math import log
from math import sqrt
from math import exp
from datetime import datetime

r = 0.05 #risk free interest

def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    if option_type == 'call':
        return S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    else:
        return K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
def find_mispriced_options(ticker, r):
    stock = yf.Ticker(ticker)
    spot_price = stock.history(period="1d")['Close'][-1]
    print(f"\nChecking options for {ticker} - Spot price: ${spot_price:.2f}")
    for expiry in stock.options[:1]:
        options_chain = stock.option_chain(expiry)
        
    
    