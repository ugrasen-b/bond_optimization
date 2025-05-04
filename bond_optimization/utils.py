# -*- coding: utf-8 -*-
"""
Created on Sun May  4 09:13:23 2025

@author: ugras
"""

def parse_maturity(maturity_str: str) -> float:
    """Convert maturity label like '1M', '2Y', '30Y' into years as float."""
    if maturity_str.endswith('M'):
        return int(maturity_str[:-1]) / 12
    elif maturity_str.endswith('Y'):
        return int(maturity_str[:-1])
    else:
        raise ValueError(f"Unknown maturity format: {maturity_str}")