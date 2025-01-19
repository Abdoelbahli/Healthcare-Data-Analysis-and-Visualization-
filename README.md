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


### 4. `app.py`

Streamlit app for interactive data exploration:
- **Patient Information Page:** Displays filtered patient information including encounters and procedures.
- **Visualizations:** Generates charts and graphs based on selected patient data for dynamic exploration.
- **Patient Report Generation:** Generates a summary report for selected patients including personal details, encounter summaries, and procedure statistics.


### 5. `log.txt`

Text file used for logging anomalies:
- Stores details about data processing issues encountered, including table names, column names, and descriptions of anomalies.

## Installation

### Requirements

- Python 3.x
- Required Python packages (specified in `requirements.txt`)
- Jupyter Notebook
- Power BI Desktop
- Streamlit

### Setup Instructions

1. Install dependencies: `pip install -r requirements.txt`
2. Run `data_processing.py` to preprocess your data.
3. Use `project.ipynb` for exploratory data analysis.
4. Import processed data into Power BI for visualization.
5. Run `app.py` with Streamlit to interactively explore patient data.

## Usage

- **Data Processing:** Modify `data_processing.py` functions to suit specific data cleaning and preprocessing requirements.
- **Exploratory Analysis:** Use `project.ipynb` to delve into data insights and refine preprocessing steps.
- **Visualization:** Create insightful dashboards and reports in Power BI based on processed data.
- **Interactive Exploration:** Use `app.py` to dynamically explore patient information and generate reports on-demand.



## Authors

- Abdellah EL BAHLI


