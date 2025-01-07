import pandas as pd
import os

def check_csv_file(file_path):
    """
    Checks if a file is a valid CSV file.
    :param file_path: Path to the file.
    :return: A message indicating if the file is valid or corrupted.
    """
    try:
        # Verify if the file exists
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        # Attempt to read the file as a CSV
        df = pd.read_csv(file_path)
        
        # If successful, display the first few rows
        print("File loaded successfully!")
        print("Preview of the file:")
        print(df.head())
        return "The CSV file is valid."
    except pd.errors.EmptyDataError:
        return "The CSV file is empty."
    except pd.errors.ParserError as e:
        return f"The CSV file is corrupted or not properly formatted. Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
file_path = "example.csv"  # Replace with your file path
status = check_csv_file(file_path)
print(status) 