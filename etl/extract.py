import pandas as pd
import requests
import os
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)

# Real ERP API Endpoints (Example: SAP S/4HANA or Oracle Cloud)
ERP_API_BASE_URL = os.getenv("ERP_API_URL", "https://your-real-erp.com/api/v1")
ERP_API_TOKEN = os.getenv("ERP_API_TOKEN", "your_super_secret_api_key")

HEADERS = {
    "Authorization": f"Bearer {ERP_API_TOKEN}",
    "Accept": "application/json"
}

def fetch_real_erp_data(endpoint):
    """Fetches live data directly from a real ERP system API"""
    url = f"{ERP_API_BASE_URL}/{endpoint}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        logging.info(f"Successfully fetched live data from {endpoint}")
        return pd.DataFrame(response.json())
    else:
        logging.error(f"Failed to fetch from ERP: {response.status_code}")
        return pd.DataFrame()

def extract_real_data():
    """Extracts live ERP data instead of using dummy CSVs"""
    logging.info("Connecting to live ERP system...")
    
    data = {
        "products": fetch_real_erp_data("products"),
        "inventory": fetch_real_erp_data("warehouses/stock"),
        "suppliers": fetch_real_erp_data("procurement/suppliers"),
        "sales": fetch_real_erp_data("orders/history")
    }
    
    return data

if __name__ == "__main__":
    # This will pull live data from your actual company ERP
    live_data = extract_real_data()
    print(live_data['inventory'].head())