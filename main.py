# -*- coding: utf-8 -*-
"""
Created on Sat May  3 21:05:00 2025

@author: ugras
"""
import pandas as pd
from bond_optimization.data_loader import load_yield_curve
from bond_optimization.portfolio import BondPortfolio

df = load_yield_curve("yc2024.csv","input")

start_date = df.index[0]
yield_curve_row = df.loc[start_date]

portfolio = BondPortfolio(initial_cash=1_000_000)

# initial investment
portfolio.invest(start_date, yield_curve_row)

for date in df.index[1:]:
    yield_curve_row = df.loc[date]
    portfolio.update(date, yield_curve_row)

history_df = pd.DataFrame(portfolio.history)
print(history_df)