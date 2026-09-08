import pandas as pd
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO)

def load_to_postgres(data: dict, db_url="postgresql://admin:password@localhost:5432/supplychain"):
    """Loads DataFrames into PostgreSQL."""
    logging.info("Starting database load...")
    
    engine = create_engine(db_url)
    
    for table_name, df in data.items():
        try:
            # We use append to not wipe seed data; change to 'replace' if you want raw CSVs to override
            df.to_sql(table_name, engine, if_exists='append', index=False)
            logging.info(f"Loaded {len(df)} rows into table: {table_name}")
        except Exception as e:
            logging.error(f"Failed to load {table_name}: {e}")

if __name__ == "__main__":
    # Test connection
    try:
        engine = create_engine("postgresql://admin:password@localhost:5432/supplychain")
        with engine.connect() as conn:
            print(conn.execute(text("SELECT version();")).fetchone())
    except Exception as e:
        print(f"DB Connection failed: {e}")