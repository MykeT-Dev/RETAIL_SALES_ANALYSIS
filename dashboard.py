import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

# 1. Page Configuration
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
st.title("Retail Sales Insight Dashboard")

DB_FILENAME = "sales_data.db"   # must match analysis_pipeline.py (DB_PATH) :contentReference[oaicite:2]{index=2}
TABLE_NAME = "sales"            # created by df.to_sql('sales', ...) :contentReference[oaicite:3]{index=3}

def get_db_path() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, DB_FILENAME)

def list_tables(conn) -> list[str]:
    rows = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
    """).fetchall()
    return [r[0] for r in rows]

# 2. Connect to Data
@st.cache_data
def load_data():
    db_path = get_db_path()

    if not os.path.exists(db_path):
        st.error(f"❌ Database not found at: {db_path}\n\nRun `analysis_pipeline.py` to generate it.")
        st.stop()

    conn = sqlite3.connect(db_path)
    try:
        tables = list_tables(conn)
        if TABLE_NAME not in tables:
            st.error(
                f"❌ Table '{TABLE_NAME}' not found in {DB_FILENAME}.\n\n"
                f"Available tables: {tables}\n\n"
                f"Run `analysis_pipeline.py` again to create/populate the table."
            )
            st.stop()

        df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn)
    except pd.errors.DatabaseError as e:
        st.error(f"❌ Error reading from SQLite: {e}")
        st.stop()
    finally:
        conn.close()

    # Normalize/validate expected columns based on analysis_pipeline.py output :contentReference[oaicite:4]{index=4}
    required = ["Transaction Date", "Location", "Item", "Quantity", "Total Spent"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(
            "❌ Your 'sales' table doesn't have the columns the dashboard expects.\n\n"
            f"Missing: {missing}\n\n"
            f"Columns found: {list(df.columns)}"
        )
        st.stop()

    # Ensure datetime for filtering
    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")
    df = df.dropna(subset=["Transaction Date"])  # remove rows that failed date parsing

    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Options")

if df.empty:
    st.error("The sales table exists, but it's empty. Please run `analysis_pipeline.py` first.")
    st.stop()

# Date Filter
start_date = df["Transaction Date"].min().date()
end_date = df["Transaction Date"].max().date()

selected_date_range = st.sidebar.date_input(
    "Select Date Range",
    [start_date, end_date],
)

# Location Filter (your pipeline uses Location, not Region) :contentReference[oaicite:5]{index=5}
locations = ["All"] + sorted(df["Location"].dropna().unique().tolist())
selected_location = st.sidebar.selectbox("Select Location", locations)

# Apply Filters
filtered_df = df.copy()

if isinstance(selected_date_range, (list, tuple)) and len(selected_date_range) == 2:
    start, end = pd.to_datetime(selected_date_range[0]), pd.to_datetime(selected_date_range[1])
    mask = (filtered_df["Transaction Date"] >= start) & (filtered_df["Transaction Date"] <= end)
    filtered_df = filtered_df.loc[mask]

if selected_location != "All":
    filtered_df = filtered_df[filtered_df["Location"] == selected_location]

# 4. KPIs (match your column names)
col1, col2, col3 = st.columns(3)
total_revenue = filtered_df["Total Spent"].sum()
txn_count = len(filtered_df)
avg_txn_value = filtered_df["Total Spent"].mean() if txn_count else 0

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Transactions", f"{txn_count:,}")
col3.metric("Avg. Transaction Value", f"${avg_txn_value:,.2f}")

st.divider()

# 5. Visualizations
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Monthly Sales Trend")
    if not filtered_df.empty:
        monthly_sales = (
            filtered_df.set_index("Transaction Date")
            .resample("M")["Total Spent"]
            .sum()
        )

        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(monthly_sales.index, monthly_sales.values, marker="o")
        ax1.set_title("Revenue over Time")
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Total Revenue ($)")
        ax1.grid(True)
        st.pyplot(fig1)
    else:
        st.warning("No data for selected filters.")

with col_chart2:
    st.subheader("Top Selling Items")
    if not filtered_df.empty:
        top_items = (
            filtered_df.groupby("Item")["Quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.bar(top_items.index, top_items.values)
        ax2.set_title("Top 5 Items by Quantity")
        ax2.set_xlabel("Item")
        ax2.set_ylabel("Quantity Sold")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig2)
    else:
        st.warning("No data for selected filters.")

# 6. Raw Data View
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
