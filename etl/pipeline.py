import logging
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.extract import extract_csvs
from etl.transform import clean_and_transform
from etl.validation import validate_data
from etl.load import load_to_postgres

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    """Master ETL pipeline runner."""
    logging.info("=== Running Supply Chain ETL Pipeline ===")
    
    # 1. Extract
    data = extract_csvs()
    if not data:
        logging.error("No data extracted. Aborting.")
        return

    # 2. Transform
    data = clean_and_transform(data)

    # 3. Validate
    if not validate_data(data):
        logging.error("Data validation failed. Aborting pipeline.")
        return

    # 4. Load
    load_to_postgres(data)
    logging.info("=== ETL Pipeline Completed Successfully ===")

if __name__ == "__main__":
    run_pipeline()