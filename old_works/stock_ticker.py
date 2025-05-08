# -*- coding: utf-8 -*-
"""
Created on Thu May  8 14:36:02 2025

@author: evert
"""

import yfinance as yf

ticker = yf.Ticker("XOM")

counter = []

while True:
    price = ticker.info['regularMarketPrice']
    print("Current price:", price)
    counter.append(1)
    if len(counter) == 10000:
            break
    



