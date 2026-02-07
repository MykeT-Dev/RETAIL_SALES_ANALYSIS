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


# LOAD DATA
print("\n--- Loading Data ---")
try:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(RAW_DATA_PATH)

    print("Data Loaded Successfully!")
    print(f"Total Rows: {df.shape[0]}")
    print(f"Total Columns: {df.shape[1]}")

    # Show the first few rows to verify
    print("\nPreview of the data:")
    print(df.head())

except FileNotFoundError:
    print(f"Error: The file '{RAW_DATA_PATH}' was not found. Please check the path and try again.")
    print("Please check the file exists in the project directory and has the correct name.")
except Exception as e:
    print(f"An error occurred while loading the data: {e}")