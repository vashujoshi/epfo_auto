import pandas as pd
import sqlite3

# Step 1: Read the CSV file into a pandas DataFrame
def read_csv_file(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # Drop the 'Action' column if it exists
        df = df.drop(columns=['Action'], errors='ignore')  # 'errors' parameter prevents error if column does not exist
        
        # Rename the columns
        df.columns = ['establishment_id', 'establishment_name', 'address', 'office_name']  # Adjust if necessary
        
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
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

# Step 3: Write the DataFrame to the SQLite table
def write_to_table(conn, df, table_name):
    try:
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Data written to table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error writing to table: {e}")

# Main logic
file_path = 'your_file.csv'  # Change this to your actual file path
db_name = 'example.db'

df = read_csv_file(file_path)
if df is not None:
    conn = create_or_connect_database(db_name)
    if conn is not None:
        write_to_table(conn, df, 'company_data')
