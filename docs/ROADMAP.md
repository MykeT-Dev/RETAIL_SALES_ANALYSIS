# Retail Sales Analysis Pipeline - Project Roadmap

## Phase 1: Environment & Configuration (Current Step)
**Goal:** Establish a stable development environment to ensure reproducibility.
* [x] **Project Directory:** Create `Retail_Sales_Analysis` folder with `/output` sub-folder.
* [x] **Virtual Environment:** Set up and activate Python `venv`.
* [ ] **Dependencies:** Install `pandas`, `sqlalchemy`, `matplotlib`, `seaborn`.
* [ ] **Configuration Script:** Create `analysis_pipeline.py` with library imports and file path constants (`RAW_DATA_PATH`, `DB_PATH`).

## Phase 2: The ETL Pipeline (Extract & Transform)
**Goal:** Convert raw, messy data into a clean, usable format.
* [ ] **Ingestion:** Load `sales_data_raw.csv` into a Pandas DataFrame.
* [ ] **Column Mapping:** Rename Kaggle columns to match the ERD schema:
    * `Transaction ID` → `TransactionID`
    * `Transaction Date` → `Date`
    * `Category` → `Product`
    * `Location` → `Region`
    * `Price Per Unit` → `Price`
    * `Quantity` → `Quantity`
* [ ] **Data Cleaning:**
    * Identify and drop rows where `Price` or `Quantity` are NULL.
    * Convert `Date` column to standard ISO 8601 format (`YYYY-MM-DD`).
    * Verify data types (ensure numeric columns are float/int).
* [ ] **Feature Engineering:** Create the `Total_Revenue` column (`Price * Quantity`).

## Phase 3: Database Storage (Load)
**Goal:** Persist the clean data into a structured SQL database for "local portability."
* [ ] **Database Connection:** specific Use `sqlalchemy` to connect to `sales_data.db` (SQLite).
* [ ] **Schema Definition:** Define the `clean_sales_records` table structure (Text, Real, Integer).
* [ ] **Data Loading:** Write the cleaned DataFrame to the SQLite database.
* [ ] **Verification:** Query the database to confirm the record count matches the cleaned DataFrame.

## Phase 4: Analysis & Reporting
**Goal:** Generate business insights and visual deliverables for the "Executive Team."
* [ ] **SQL Analysis:**
    * **Query 1:** Calculate Total Revenue by Region.
    * **Query 2:** Identify Top 5 Best-Selling Products.
    * **Query 3:** Calculate Monthly Revenue Trends (Time-Series).
* [ ] **Visualization (Python):**
    * Create a **Bar Chart** for Top Products.
    * Create a **Line Chart** for Monthly Revenue.
* [ ] **Export:** Save all charts as high-resolution PNG files to the `/output` folder.

## Phase 5: Documentation & Portfolio Polish
**Goal:** Package the code as a professional software product.
* [ ] **README.md:** Finalize the project overview, installation instructions, and usage guide.
* [ ] **Artifacts:** Ensure DFD and ERD images are saved in a `docs/` folder and linked in the README.
* [ ] **Requirements:** Run `pip freeze > requirements.txt` to capture exact library versions.
* [ ] **Git:** Initialize repository, create `.gitignore` (exclude `venv/` and `__pycache__/`), and push to GitHub.