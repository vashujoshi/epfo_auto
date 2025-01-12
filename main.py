import time
import glob
import os
from django.shortcuts import render
from nanodjango import Django
import pandas as pd
from scrapper import setup_driver, search_and_download_excel
from db_func import read_csv_file, create_or_connect_database, write_to_table
from checker import check_excel_file
import pandas as pd
import sqlite3
from xlsx2csv import Xlsx2csv

company_name = ""
# Initialize NanoDjango
app = Django(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'pf_tracker.db',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.messages',
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(os.getcwd(), 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }
    ],
    STATICFILES_DIRS=[
        os.path.join(os.getcwd(), 'static'),
    ],
    STATIC_URL='/static/',
)

def get_latest_file(directory, extension="*.csv"):
    """Get the most recently modified file in a directory."""
    files = glob.glob(os.path.join(directory, extension))
    if not files:
        return None
    return max(files, key=os.path.getmtime)

@app.route("/")
def home(request):
    return render(request, 'home.html')

@app.route("/search")
def search(request):
    """Handle the search, scrape data, and store it in the database."""
    global company_name
    if "company_name" not in request.GET:
        return render(request, "home.html", {"error": "Please enter a company name.", "success": False})

    company_name = request.GET["company_name"].strip()
    if not company_name:
        return render(request, "home.html", {"error": "Company name cannot be empty.", "success": False})

    download_dir = os.path.join(os.getcwd(), "CompanyList")
    print(f"Download directory is: {download_dir}")
    os.makedirs(download_dir, exist_ok=True)  # Ensure directory exists

    driver = None
    try:
        # Step 1: Initialize the driver and download the file
        driver = setup_driver(download_dir)
        file_path = search_and_download_excel(driver, company_name, download_dir)
        print("file_path just before df", file_path)
        check_excel_file(file_path)
        df = pd.read_csv(file_path)
        print("workbook", df.head())
        print("file_path just before df", file_path)
        # Step 2: Ensure the file exists or fetch the latest one
        if not os.path.exists(file_path):
            file_path = get_latest_file(download_dir, "*.csv")
            if not file_path:
                return render(request, "home.html", {"error": "No valid CSV file found.", "success": False})

        # Step 3: Read the downloaded CSV file
        df = pd.read_csv(file_path)
        if df is None:
            return render(request, "home.html", {"error": "Failed to read the downloaded CSV file.", "success": False})

        # Step 4: Connect to the SQLite database
        conn = create_or_connect_database("pf_tracker.db")
        if conn is None:
            return render(request, "home.html", {"error": "Database connection failed.", "success": False})

        # Step 5: Write the data to the database
        write_to_table(conn, df, "company_data")

        # Close the database connection
        conn.close()

        # Insert the data into the database
        insert_to_db()
    
        return render(request, "home.html", {"success": True, "file_path": file_path})
    except Exception as e:
        return render(request, "home.html", {"error": f"An error occurred: {e}", "success": False})
    finally:
        if driver:
            driver.quit()  # Safely quit the driver


def insert_to_db():
    try:
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()

        # Read CSV file into a pandas DataFrame
        extn = '.csv'
        filename = company_name + extn
        download_path = r"C:\Users\Jai Mata di\Desktop\allprograms\automate\CompanyList\\"
        df = pd.read_csv(download_path + filename)
        df.to_sql('company_details', sqliteConnection, if_exists='append', index=False)

        # Commit the changes
        sqliteConnection.commit()

        # Close the connection
        sqliteConnection.close()
    except Exception as e:
            print(f"Error: {e}")
            return f"The file is corrupted or invalid. Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0:8004")
