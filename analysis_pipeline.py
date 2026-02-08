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

# Clean Data
print("\n--- Cleaning Data ---")

# Fill missing discounts with False
df['Discount Applied'] = df['Discount Applied'].fillna(False)

# Drop rows where critical data is missing
df = df.dropna(subset=['Item', 'Price Per Unit', 'Quantity', 'Total Spent'])

# Convert 'Transaction Date' to datetime format
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])

# Fix data types
df['Price Per Unit'] = df['Price Per Unit'].astype(float)
df['Quantity'] = df['Quantity'].astype(int)
df['Total Spent'] = df['Total Spent'].astype(float)

print("Data Cleaning Completed!")
print(f"Rows remaining: {df.shape[0]}")


# INSPECT DATA
print("\n--- Inspecting Data ---")    
print("\nData Types & Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nStatistical Summary:")
print(df.describe())

# ANALYZE DATA
print("\n--- Analysis Results ---")

# 1. Monthly Sales
# Create a new column 'Month' formatted as 'YYYY-MM'
# We use .dt. to_period('M') to handle dates easily
df['Month'] = df['Transaction Date'].dt.to_period('M')

# Group by Month and sum the 'Total Spent'
monthly_sales = df.groupby('Month')['Total Spent'].sum()

print("\nTotal Sales by Month:")
print(monthly_sales)

# 2. Top 5 Items by Quantity Sold
top_items = df.groupby('Item')['Quantity'].sum().sort_values(ascending=False).head(5)

print("\nTop 5 Best-Selling Items:")
print(top_items)

# 3. Sales by Location
location_sales = df.groupby('Location')['Total Spent'].sum().sort_values(ascending=False)

print("\nSales by Location:")
print(location_sales)