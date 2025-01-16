
import pandas as pd

def load_csv_file(file_path, separator=None):
    """
    Reads a single CSV file with handling for different encodings and separators.
    
    Parameters:
    file_path (str): The path to the CSV file.
    separator (str, optional): The separator used in the CSV file. If not provided, will prompt the user.
    
    Returns:
    pd.DataFrame: The DataFrame containing the CSV data.
    """
    encodings = ['utf-8', 'latin1', 'ISO-8859-1']
    default_separators = [',', ';', '\t', '|', ':']
    separators = [separator] if separator else default_separators
    
    for encoding in encodings:
        for sep in separators:
            try:
                df = pd.read_csv(file_path, encoding=encoding, sep=sep)
                print(f"Successfully read the file with encoding {encoding} and separator '{sep}'")
                return df
            except UnicodeDecodeError:
                continue
            except pd.errors.ParserError:
                continue
    
    if not separator:
        # If none of the default combinations work, prompt the user for a separator
        user_sep = input(f"Could not read the file with common separators. Please provide the separator used in {file_path}: ")
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding, sep=user_sep)
                print(f"Successfully read the file with encoding {encoding} and user-provided separator '{user_sep}'")
                return df
            except UnicodeDecodeError:
                continue
            except pd.errors.ParserError:
                continue
    
    # If none of the user-provided combinations work, raise an error
    raise ValueError(f"Could not read the file {file_path} with provided encodings and separator.")






def display_df_insights(df):
    """
    Displays various insights about a DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    """
    print("Data Types of Columns:\n", df.dtypes)
    print("\nCount of Null Values in Each Column:\n", df.isnull().sum())
    print("\nDataFrame Info:")
    df.info()
    print("\nAny Null Values in DataFrame: ", df.isnull().values.any())
    #print("\nRows with Any Null Values:\n", df[df.isnull().any(axis=1)])
    print("\nColumns with Any Null Values:\n", df.columns[df.isnull().any()])




def display_unique_values(df, columns):
    """
    Displays the unique values for specified columns in a DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    columns (list): The list of columns to get unique values from.
    """
    for column in columns:
        if column in df.columns:
            print(f"Unique values in column '{column}':")
            print(df[column].unique())
            print("\n")
        else:
            print(f"Column '{column}' does not exist in the DataFrame.\n")



def log_issue(logs, table_name, column_name, description):
    logs.append([table_name, column_name, description])
################################################################# CONVERT TO STUFF #####################################

def convert_columns_to_int(df, columns, table_name, logs):
    """
    Converts specified columns to integer type and logs the action.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    columns (list): The list of columns to convert to integers.
    table_name (str): The name of the table being processed.
    logs (list): The list to log actions.
    
    Returns:
    pd.DataFrame: The DataFrame with specified columns converted to integers.
    """
    for column in columns:
        if column in df.columns:
            try:
                df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0).astype(int)
                log_issue(logs, table_name, column, 'Should be Converted to integer')
            except Exception as e:
                log_issue(logs, table_name, column, f'Error converting to integer: {e}')
        else:
            log_issue(logs, table_name, column, 'Column does not exist in the DataFrame')
    
    return df

def convert_column_to_float(df, column_name, table_name, logs):
    """
    Converts a column to float and logs the action.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    column_name (str): The column to convert.
    table_name (str): The name of the table being processed.
    logs (list): The list to log actions.
    
    Returns:
    pd.DataFrame: The modified DataFrame.
    """
    if column_name in df.columns:
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce').astype(float)
        log_issue(logs, table_name, column_name, 'Object type should be Converted to float')
    else:
        log_issue(logs, table_name, column_name, 'Column does not exist in the DataFrame')
    return df

##################### DATE TRANSFORMING STUFF ########################################################################

from datetime import datetime

def convert_to_date(df, column_name, table_name, logs=None):
    """
    Converts a column to datetime format with error handling and logging.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    column_name (str): The name of the column containing date strings.
    table_name (str): The name of the table being processed.
    logs (list, optional): A list to log any issues encountered during conversion.
    
    Returns:
    pd.DataFrame: The modified DataFrame.
    """
    if logs is None:
        logs = []
    
    try:
        df[column_name] = pd.to_datetime(df[column_name], format='%Y-%m-%d', errors='coerce')
        log_issue(logs, table_name, column_name, 'should be converted to datetime format.')
    except Exception as e:
        log_issue(logs, table_name, column_name, f'Error converting to datetime format: {str(e)}')
    
    return df



def convert_date_format(df, column_name, table_name, logs=None):
    """
    Converts a column containing custom date strings to 'YYYY-MM-DD' format with error handling and logging.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    column_name (str): The name of the column containing date strings.
    table_name (str): The name of the table being processed.
    logs (list, optional): A list to log any issues encountered during conversion.
    
    Returns:
    pd.DataFrame: The modified DataFrame.
    """
    if logs is None:
        logs = []
    
    def convert_string_to_date(date_str):
        try:
            # Split the string by '|' and '-' to extract year, month, and day
            parts = date_str.split('|')
            year = parts[0]
            month_day = parts[1].split('-')
            month = month_day[0]
            day = month_day[1]
            
            # Construct the date in 'YYYY-MM-DD' format
            formatted_date = f'{year}-{month}-{day}'
            log_issue(logs, table_name, column_name, f'should be converted to datetime format')
            return formatted_date
        except Exception as e:
            log_issue(logs, table_name, column_name, f'Error converting date string {date_str}: {str(e)}')
            return pd.NaT
    
    df[column_name] = df[column_name].apply(convert_string_to_date)
    return df


# Function to convert a string to datetime
def convert_string_to_date(date_str):
    date_str = date_str.replace('|', '-')
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')

# Function to convert a column to datetime
def convert_column_to_date(df, column_name, table_name, logs):
    if column_name in df.columns:
        try:
            df[column_name] = pd.to_datetime(df[column_name], format='%Y-%m-%dT%H:%M:%SZ')
            log_issue(logs, table_name, column_name, 'Object type should be Converted to datetime')
        except Exception as e:
            df[column_name] = df[column_name].apply(convert_string_to_date)
            log_issue(logs, table_name, column_name, 'Object type should be Converted to datetime')
    else:
        log_issue(logs, table_name, column_name, 'Column does not exist in the DataFrame')
    return df

###############################################THE END OF DATE STUFF ########################################################

def preprocess_columns(df, columns):
    """
    Strips whitespace, converts to uppercase for specified columns in a DataFrame, and removes duplicates.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to preprocess.
    columns (list): The list of columns to preprocess.
    
    Returns:
    pd.DataFrame: The preprocessed DataFrame.
    """
    for column in columns:
        if column in df.columns:
            # Strip whitespace and convert to uppercase
            df[column] = df[column].astype(str).str.strip().str.upper()
        else:
            print(f"Column '{column}' does not exist in the DataFrame.\n")
    
    # Remove duplicates
    df = df.drop_duplicates(subset=columns)
    
    return df


import numpy as np

def replace_value_with_nan(df, column, value_to_replace):
    """
    Replaces a specific value in a specified column with NaN.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    column (str): The column in which to replace the value.
    value_to_replace (any): The value to replace with NaN.
    
    Returns:
    pd.DataFrame: The DataFrame with the specified value replaced by NaN in the specified column.
    """
    if column in df.columns:
        df[column] = df[column].replace(value_to_replace, np.nan)
    else:
        print(f"Column '{column}' does not exist in the DataFrame.")
    
    return df


def replace_nan_with_value(df, columns, table_name, logs, replacement_value="VALUE NOT PROVIDED"):
    """
    Replaces NaN values in specified columns with a given value and logs the action.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    columns (list): The list of columns in which to replace NaN values.
    table_name (str): The name of the table being processed.
    logs (list): The list to log actions.
    replacement_value (str): The value to replace NaN with.
    
    Returns:
    pd.DataFrame: The DataFrame with NaN values replaced by the specified value in the specified columns.
    """
    for column in columns:
        if column in df.columns:
            df[column] = df[column].fillna(replacement_value)
            log_issue(logs, table_name, column, f'NaN values should be replaced with "{replacement_value}"')
        else:
            log_issue(logs, table_name, column, 'Column does not exist in the DataFrame')
    
    return df


def replace_nan_in_numeric_columns(df, table_name, logs):
    """
    Replaces NaN values in all numerical columns of a DataFrame with 0 and logs the action.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    table_name (str): The name of the table being processed.
    logs (list): The list to log actions.
    
    Returns:
    pd.DataFrame: The DataFrame with NaN values replaced by 0 in numerical columns.
    """
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    for column in numeric_columns:
        log_issue(logs, table_name, column, 'NaN values should be replaced with 0')
    
    return df




def save_df_to_csv(df, file_path):
    """
    Saves a DataFrame to a CSV file.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to save.
    file_path (str): The path where the CSV file will be saved.
    
    Returns:
    None
    """
    try:
        df.to_csv(file_path, index=False)
        print(f"DataFrame saved to {file_path} successfully.")
    except Exception as e:
        print(f"An error occurred while saving the DataFrame to CSV: {e}")
