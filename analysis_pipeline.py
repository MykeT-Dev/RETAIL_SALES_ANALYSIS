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

# LOAD TO DATABASE
print("\n--- Saving to Database ---")

# FIX: Convert 'Month' from a Period object to a String so SQLite can understand it
df['Month'] = df['Month'].astype(str)

# 1. Create the Database Engine
engine = db.create_engine(f'sqlite:///{DB_PATH}')

try:
    # 2. Write the DataFrame to SQL
    df.to_sql('sales', engine, if_exists='replace', index=False)
    
    print(f"Data successfully saved to '{DB_PATH}'")
    
    # 3. Verify by Querying
    with engine.connect() as connection:
        result = connection.execute(db.text("SELECT COUNT(*) FROM sales"))
        count = result.scalar()
        print(f"Database Row Count Verification: {count}")

except Exception as e:
    print(f"Error saving to database: {e}")# LOAD TO DATABASE
print("\n--- Saving to Database ---")

# FIX: Convert 'Month' from a Period object to a String so SQLite can understand it
df['Month'] = df['Month'].astype(str)

# 1. Create the Database Engine
engine = db.create_engine(f'sqlite:///{DB_PATH}')

try:
    # 2. Write the DataFrame to SQL
    df.to_sql('sales', engine, if_exists='replace', index=False)
    
    print(f"Data successfully saved to '{DB_PATH}'")
    
    # 3. Verify by Querying
    with engine.connect() as connection:
        result = connection.execute(db.text("SELECT COUNT(*) FROM sales"))
        count = result.scalar()
        print(f"Database Row Count Verification: {count}")

except Exception as e:
    print(f"Error saving to database: {e}")


#VISUALIZE DATA
import matplotlib.pyplot as plt

print("\n--- Visualizing Data ---")

# Set the style to be clean and professional
# (If 'ggplot' doesn't work for you, you can remove this line or choose another style)
plt.style.use('ggplot')

# --- Filter out the incomplete last month for a cleaner visualization ---
# we use .iloc[:-1] to exclude the last row which is likely incomplete
monthly_sales = monthly_sales.iloc[:-1]
print("\nNote: The last month has been excluded from the monthly sales trend visualization to avoid skewing the results with incomplete data.")

# 1. Monthly Sales Trend (Line Chart)
plt.figure(figsize=(10, 6))

#convert the 'Month' column back to datetime for plotting
monthly_sales.index = pd.to_datetime(monthly_sales.index.astype(str))
monthly_sales.plot(kind='line', marker='o', color='blue', linewidth=2)
plt.title('Monthly Sales Trend', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/monthly_sales_trend.png')
print(f'\nSaved: {OUTPUT_DIR}/monthly_sales_trend.png')

# 2. Top 5 Items by Quantity Sold (Bar Chart)
plt.figure(figsize=(10, 6))
top_items.plot(kind='bar', color='green')
plt.title('Top 5 Best-Selling Items by Quantity', fontsize=16)
plt.xlabel('Item', fontsize=12)
plt.ylabel('Quantity Sold', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/top_5_items.png')
print(f'Saved: {OUTPUT_DIR}/top_5_items.png')

# 3. Sales by Location (Pie Chart)
plt.figure(figsize=(8, 8))
location_sales.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
plt.title('Sales Distribution: Online vs In-Store', fontsize=16)
plt.ylabel('')  # Hide the y-label for a cleaner look
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/sales_by_location.png')
print(f'Saved: {OUTPUT_DIR}/sales_by_location.png')

print("\n--- Pipeline Completed Successfully! ---")