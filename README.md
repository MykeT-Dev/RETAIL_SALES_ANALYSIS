# Retail Sales Analysis Pipeline

**A full-stack data engineering pipeline that extracts raw sales data, cleans and transforms it using Python, loads it into a SQL database, and generates automated visualization reports.**

---

## Project Overview
This project simulates a real-world Data Engineering workflow. The goal was to take raw, messy retail sales data and convert it into actionable business insights.

**Key Accomplishments:**
* **ETL Pipeline:** Built a robust extraction, transformation, and loading process.
* **Data Quality:** Implemented automated cleaning logic to handle missing values and correct data types.
* **Database Integration:** Designed a persistent SQLite database storage layer.
* **Automated Reporting:** Generated trend analysis charts using Matplotlib.

## Tech Stack
* **Language:** Python 3.11
* **Data Manipulation:** Pandas
* **Database:** SQLite / SQLAlchemy
* **Visualization:** Matplotlib
* **Version Control:** Git / GitHub

## Architecture
The pipeline follows a standard ETL (Extract, Transform, Load) architecture:
1.  **Ingest:** Read raw CSV data (`sales_data_raw.csv`).
2.  **Clean:** Remove nulls, cast types, and handle missing business logic.
3.  **Load:** Save structured data into `sales_data.db`.
4.  **Analyze & Visualize:** Aggregate metrics and generate PNG reports.

*(See [ARCHITECTURE.md](ARCHITECTURE.md) for the detailed system diagram)*

## Key Insights
After processing **11,000+ transaction records**, the analysis revealed:
* **Sales Trends:** Monthly sales have remained steady, with a slight dip in early 2025.
* **Top Products:** "Beverages" and "Milk Products" are the highest volume categories.
* **Location Analysis:** Online sales ($749k) are slightly outperforming In-Store sales ($723k).

## How to Run This Project
*Note: These steps are for setting up the project on a new machine.*

**1. Clone the repository**
```bash
git clone [https://github.com/MykeT-Dev/Retail_Sales_Analysis.git](https://github.com/MykeT-Dev/Retail_Sales_Analysis.git)
cd Retail_Sales_Analysis
```

**2. Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install Dependencies**
```bash
pip install pandas sqlalchemy matplotlib
```

**4. Run the Pipeline**
```bash
python analysis_pipeline.py
```

**5. Check the Results**
* **Database:** `sales_data.db` (Use a SQLite viewer to inspect)
* **Charts:** Open the `output/` folder to see generated graphs.

---
**Author:** Myke Turza