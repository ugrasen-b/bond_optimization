# -*- coding: utf-8 -*-
"""
Created on Sun May  4 08:58:55 2025

@author: ugras
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict
import pandas as pd
from .utils import parse_maturity
class BondHolding(BaseModel):
    maturity_date: pd.Timestamp
    amount: float
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
class BondPortfolio(BaseModel):
    initial_cash: float = Field(..., gt=0)
    cash: float = 0
    holdings: List[BondHolding] = Field(default_factory=list)
    history: List[Dict] = Field(default_factory=list)
    max_bonds: int = 4
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def invest(self, date: pd.Timestamp, yield_curve_row: pd.Series):
        # pick top N yields
        selected = yield_curve_row.nlargest(self.max_bonds)

        amount_per_bond = (self.cash if self.cash > 0 else self.initial_cash) / len(selected)

        for maturity_str, rate in selected.items():
            # maturity = int(maturity_str)  # convert '1', '2' to integer years
            maturity_years = parse_maturity(maturity_str)
            months = int(maturity_years * 12)
            maturity_date = date + pd.DateOffset(months=months)
            # maturity_date = date + pd.DateOffset(years=maturity_years)
            # maturity_date = date + pd.DateOffset(years=maturity)
            payoff = amount_per_bond * (1 + rate/100 * maturity_years)

            self.holdings.append(BondHolding(
                maturity_date=maturity_date,
                amount=payoff
            ))

        self.cash = 0
        
    def update(self, current_date: pd.Timestamp, yield_curve_row: pd.Series):
        # collect matured bonds
        matured = [h for h in self.holdings if h.maturity_date <= current_date]
        for bond in matured:
            self.cash += bond.amount

        # remove matured from holdings
        self.holdings = [h for h in self.holdings if h.maturity_date > current_date]

        if self.cash > 0:
            self.invest(current_date, yield_curve_row)

        portfolio_value = self.cash + sum(h.amount for h in self.holdings)
        self.history.append({'date': current_date, 'value': portfolio_value})