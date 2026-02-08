# System Architecture: Retail Sales Analysis Pipeline

**Project:** Retail Sales Analysis Pipeline
**Date:** February 8, 2026
**Author:** Myke Turza

## Data Flow Diagram

The following diagram illustrates the end-to-end flow of data from ingestion to reporting.

```mermaid
graph LR
    %% Define Nodes
    RawData["sales_data_raw.csv<br/>(Raw Source)"]
    
    subgraph "ETL Pipeline (Python)"
        Ingest["Ingest Data<br/>(Pandas)"]
        Clean["Clean & Transform<br/>(Drop Nulls, Cast Types)"]
        Analyze["IQ Calculate Metrics<br/>(Aggregations)"]
    end
    
    DB[("SQLite Database<br/>sales_data.db")]
    
    subgraph "Outputs"
        Charts["Visualizations<br/>(.png)"]
        Report["Summary Report<br/>(.xlsx / .txt)"]
    end

    %% Define Edges (Connections)
    RawData --> Ingest
    Ingest --> Clean
    Clean --> Analyze
    
    Analyze -->|Load Clean Data| DB
    Analyze -->|Generate| Charts
    Analyze -->|Export| Report

    %% Styling with Black Text
    style RawData fill:#f9f,stroke:#333,stroke-width:2px,color:#000
    style DB fill:#ccf,stroke:#333,stroke-width:2px,color:#000
    style Ingest fill:#ff9,stroke:#333,color:#000
    style Clean fill:#ff9,stroke:#333,color:#000
    style Analyze fill:#ff9,stroke:#333,color:#000