import pandas as pd

def read_file(file_path):
    """
    Check file type (CSV or Excel) based on the file extension
    and convert it to a Pandas DataFrame.
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")
    
    return df


def convert_file(df, column_name):
    """
    Convert the specified column of a DataFrame into a list.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")

    df[column_name] = "https://" + df[column_name]
    column_list = df[column_name].tolist()

    return column_list
