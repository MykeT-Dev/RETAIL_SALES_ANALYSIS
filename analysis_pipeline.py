import pandas as pd
import sqlalchemy as db
import sqlite3
import os

# CONFIGURATION
RAW_DATA_PATH = 'sales_data_raw.csv'
DB_PATH = 'sales_data.db'
OUTPUT_DIR = 'output'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("--- Environment Setup Complete ---")
print(f"Pandas version: {pd.__version__}")
print(f"SQLAlchemy version: {db.__version__}")
