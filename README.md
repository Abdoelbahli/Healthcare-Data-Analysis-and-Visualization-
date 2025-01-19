# Healthcare Data Analysis and Visualization

## Overview

This project focuses on processing healthcare data, performing analysis, and visualizing insights using various tools and frameworks.

## Components

### 1. `data_processing.py`

This Python script handles the core data processing tasks:
- **Loading Data:** Reads CSV files with support for different encodings and separators.
- **Data Insights:** Provides functions to display data types, null values, and basic information about the DataFrame.
- **Data Cleaning:** Functions for converting data types, handling missing values, and preprocessing columns.
- **Logging Anomalies:** Logs issues encountered during data processing to a text file (`log.txt`).


### 2. `project.ipynb`

Jupyter notebook used for:
- Calling functions from `data_processing.py` to preprocess data.
- Exploratory Data Analysis (EDA) to understand data distributions and relationships.
- Iterative development and testing of data processing logic.

### 3. Power BI Visualization `Dashboard`

Power BI used for creating interactive visualizations:
- **Key Performance Indicators (KPIs):** Metrics such as Average Cost per Visit, Average Length of Stay, etc., derived from processed data.
- **Dashboard Creation:** Visual representations of patient demographics, encounter statistics, and procedure trends.
