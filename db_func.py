import csv
import pandas as pd
import sqlite3

# def read_csv_file(file_path):
#     try:
#         df = pd.read_csv(file_path)
        
#         # Drop the 'Action' column if it exists
#         df = df.drop(columns=['Action'], errors='ignore')  # 'errors' parameter prevents error if column does not exist
        
#         # Rename the columns
#         df.columns = ['establishment_id', 'establishment_name', 'address', 'office_name']  # Adjust if necessary
        
#         return df
#     except Exception as e:
#         print(f"Error reading CSV file: {e}")
#         return None
def read_csv_file(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            # check
            print(f"Column names in CSV: {reader.fieldnames}")  

            # csv col to keys ma krdiya
            records = []
            for row in reader:
                row.pop('Action', None)  # Remove 'Action' column if present
                records.append({
                    'establishment_id': row['Establishment ID'],
                    'establishment_name': row['Establishment Name'],
                    'address': row['Address'],
                    'office_name': row['Office Name']
                })
            return records
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []



def write_to_company_data(df, Company_Data):
    try:
        for _, row in df.iterrows():
           Company_Data.objects.create(
                establishment_id=row['establishment_id'],
                establishment_name=row['establishment_name'],
                address=row['address'],
                office_name=row['office_name']
           )
        print("Data written to 'company_data' table successfully.")
    except Exception as e:
        print(f"Error writing to 'company_data' table: {e}")

def read_csv_file2(file_path, company_name):
    try:
        file_path = file_path.replace(" ","\ ")
        df = pd.read_csv(file_path)
        df.columns = ['TRRN', 'Date Of Credit', 'Amount', 'Wage Month', 'No. of Employee', 'ECR']
        df.insert(0, 'Company_Name', company_name)  # Insert company_name as the first column
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def write_to_payment_detail(df, Payment_Detail):
    try:
        # Convert the date format to the expected format
        df['Date Of Credit'] = pd.to_datetime(df['Date Of Credit'], format='%d-%b-%Y %H:%M:%S').dt.strftime('%Y-%m-%d %H:%M:%S')
        
        for _, row in df.iterrows():
            Payment_Detail.objects.create(
                company_name=row['Company_Name'],
                trrn=row['TRRN'],
                date_of_credit=row['Date Of Credit'],
                amount=row['Amount'],
                wage_month=row['Wage Month'],
                no_of_employee=row['No. of Employee'],
                ecr=row['ECR']
            )
        print("Data written to 'payment_detail' table successfully.")
    except Exception as e:
        print(f"Error writing to 'payment_detail' table: {e}")
