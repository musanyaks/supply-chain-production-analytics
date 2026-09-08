import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

def clean_and_transform(data: dict) -> dict:
    """Cleans and transforms raw data."""
    logging.info("Starting data transformation...")
    
    # 1. Clean Products
    if 'products' in data:
        df = data['products']
        df['unit_cost'] = pd.to_numeric(df['unit_cost'], errors='coerce').fillna(0.0)
        df['holding_cost'] = pd.to_numeric(df['holding_cost'], errors='coerce').fillna(0.0)
        data['products'] = df

    # 2. Clean Sales and parse dates
    if 'sales' in data:
        df = data['sales']
        df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
        df['quantity'] = df['quantity'].fillna(0).astype(int)
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce').fillna(0.0)
        df.dropna(subset=['sale_date'], inplace=True)
        data['sales'] = df

    # 3. Clean Procurement
    if 'procurement' in data:
        df = data['procurement']
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df['expected_delivery'] = pd.to_datetime(df['expected_delivery'], errors='coerce')
        data['procurement'] = df

    logging.info("Data transformation complete.")
    return data

if __name__ == "__main__":
    # Quick test
    from extract import extract_csvs
    raw = extract_csvs()
    transformed = clean_and_transform(raw)