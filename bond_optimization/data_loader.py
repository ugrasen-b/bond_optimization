# -*- coding: utf-8 -*-
"""
Created on Sat May  3 21:02:37 2025

@author: ugras
"""

import pandas as pd
import os
from bond_optimization.config import EXPECTED_COLUMNS

def load_yield_curve(filename="", data_dir="../input"):
    """
    Loads and validates yield curve data from CSV.

    Returns:
        pd.DataFrame: Cleaned yield curve data.
    Raises:
        ValueError: If required columns are missing.
    """
    filepath = os.path.join(data_dir, filename)
    df = pd.read_csv(filepath)

    # Ensure Date column exists
    if 'Date' not in df.columns:
        raise ValueError("Input data must have a 'Date' column.")

    # Parse Date
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    if df['Date'].isnull().all():
        raise ValueError("No valid dates found in 'Date' column.")

    df = df.set_index('Date')

    # Clean column names
    df.columns = [col.strip().replace(' ', '').replace('Mo', 'M').replace('Yr', 'Y') for col in df.columns]

    # Filter columns: only keep expected columns that exist
    missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}\nPlease check the input data.")

    # Keep only expected columns (in correct order)
    df = df[EXPECTED_COLUMNS]

    # Handle missing values → here we can fill forward or drop, depending on your strategy
    if df.isnull().values.any():
        print("⚠️ Warning: Missing values detected. Filling forward...")
        df = df.ffill()
        
    df = df.resample('ME').first()
    
    return df