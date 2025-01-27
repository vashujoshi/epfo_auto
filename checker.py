import pandas as pd
from xlsx2csv import Xlsx2csv

def check_excel_file(file_path):
    try:
        # Try to read the Excel file using openpyxl
        df = pd.read_excel(file_path, engine='openpyxl')
        if(df.head().empty):
            return "No records available for the company."
        print("File loaded successfully using openyxl!")
        print("Preview of the file:")
        print(df.head())
        return "The Excel file is valid."
    except Exception as e:
        print(f"Error reading Excel file: {e}. Trying to read as CSV.")
        try:
            # Convert the Excel file to CSV and read it
            csv_file_path = file_path.replace(".xlsx", ".csv")
            Xlsx2csv(file_path, outputencoding="utf-8").convert(csv_file_path)
            df = pd.read_csv(csv_file_path)
            print("File loaded successfully as CSV yeah !")
            print("Preview of the file:")
            print(df.head())
            return "The file is valid and was read as CSV."
        except Exception as e:
            print(f"Error: {e}")
            return f"The file is corrupted or invalid. Error: {e}"

if __name__ == "__main__":
    file_path = "CompanyList/test.xlsx"
    status = check_excel_file(file_path)
    print(status)