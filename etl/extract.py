import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)

def extract_csvs(raw_dir='data/raw'):
    """Extracts all raw CSV files into a dictionary of DataFrames."""
    logging.info("Starting data extraction...")
    data = {}
    
    required_files = [
        'products.csv', 'suppliers.csv', 'customers.csv', 
        'inventory.csv', 'procurement.csv', 'production.csv', 
        'sales.csv', 'deliveries.csv'
    ]
    
    for file in required_files:
        path = os.path.join(raw_dir, file)
        if os.path.exists(path):
            key = file.split('.')[0]
            data[key] = pd.read_csv(path)
            logging.info(f"Extracted {file} with {len(data[key])} rows.")
        else:
            logging.warning(f"File {file} not found in {raw_dir}. Skipping.")
            
    return data

if __name__ == "__main__":
    data = extract_csvs()
    for k, v in data.items():
        print(f"{k}: {v.shape}")