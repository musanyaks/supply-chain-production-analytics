import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def validate_data(data: dict) -> bool:
    """Validates data quality before loading."""
    logging.info("Starting data validation...")
    is_valid = True
    
    if 'products' in data:
        if data['products']['sku'].duplicated().any():
            logging.error("Validation Failed: Duplicate SKUs found in products.")
            is_valid = False
        if (data['products']['unit_cost'] < 0).any():
            logging.error("Validation Failed: Negative unit cost found in products.")
            is_valid = False
            
    if 'sales' in data:
        if data['sales']['quantity'].isnull().any():
            logging.error("Validation Failed: Null quantities in sales data.")
            is_valid = False

    if is_valid:
        logging.info("Data validation passed successfully.")
    return is_valid