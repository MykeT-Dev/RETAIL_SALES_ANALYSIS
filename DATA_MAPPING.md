# Source-to-Target Mapping: Retail Sales Data

**Project:** Retail Sales Analysis Pipeline
**Date:** February 8, 2026
**Author:** Myke Turza

## Overview
This document defines the transformation logic for cleaning raw sales data (`sales_data_raw.csv`) before analysis.

## Field Mapping & Transformation Logic

| Source Column | Target Column | Data Type | Transformation Logic | Missing Data Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Transaction ID** | `Transaction ID` | String | None. | **Error:** Row must be dropped if ID is missing. |
| **Transaction Date** | `Transaction Date` | Datetime | Convert from string to datetime object. | **Error:** Row must be dropped if date is invalid. |
| **Customer ID** | `Customer ID` | String | None. | Allow NULLs (Guest checkouts). |
| **Category** | `Category` | String | None. | **Error:** Row dropped if missing. |
| **Item** | `Item` | String | None. | **Error:** Row dropped if missing. |
| **Price Per Unit** | `Price Per Unit` | Float | Cast to float. Ensure > 0. | **Error:** Row dropped if missing. |
| **Quantity** | `Quantity` | Integer | Cast to integer. Ensure > 0. | **Error:** Row dropped if missing. |
| **Total Spent** | `Total Spent` | Float | Cast to float. | **Error:** Row dropped if missing. |
| **Discount Applied** | `Discount Applied` | Boolean | Convert to Boolean (True/False). | **Impute:** If NULL, assume `False`. |
| **Location** | `Location` | String | None. | **Error:** Row dropped if missing. |