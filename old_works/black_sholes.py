# -*- coding: utf-8 -*-
"""
Created on Mon May  5 13:04:06 2025

@author: evert
"""

from scipy.stats import norm
from math import log
from math import sqrt
from math import exp


def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    if option_type == 'call':
        return S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    else:
        return K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    
    