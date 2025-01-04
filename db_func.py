import pandas as pd
import sqlite3

# Step 1: Read the Excel file into a pandas DataFrame
def read_excel_file(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

# Step 2: Create or connect to an SQLite database
def create_or_connect_database(db_name="example.db"):
    try:
        conn = sqlite3.connect(db_name)
        print("Connected to SQLite database.")
        return conn
    except Exception as e:
        print(f"Error connecting to SQLite database: {e}")
        return None


# Step 4: Write the DataFrame to the SQLite table
def write_to_table(conn, df, table_name):
    try:
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Data written to table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error writing to table: {e}")