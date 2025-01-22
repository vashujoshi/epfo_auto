import time
import glob
import os
import webbrowser
from django.shortcuts import render, redirect
from nanodjango import Django
import pandas as pd
from scrapper import setup_driver, search_and_download_excel
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrapper_final import epfs_scraper
from db_func import read_csv_file, create_or_connect_database, write_to_table,read_csv_file2
from checker import check_excel_file
import pandas as pd
import sqlite3

company_name = ""

# Initialize NanoDjango
app = Django(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'company_pf_details.db',
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
    if "company_name" not in request.GET:
        return render(request, "home.html", {"error": "Please enter a company name.", "success": False})

    company_name = request.GET["company_name"].strip()
    if not company_name:
        return render(request, "home.html", {"error": "Company name cannot be empty.", "success": False})

    download_dir = os.path.join(os.getcwd(), "CompanyList")
    os.makedirs(download_dir, exist_ok=True)  # Ensure directory exists

    driver = None
    try:
        # Initialize the driver
        driver = setup_driver(download_dir)
        
        # Perform search and download
        file_path = search_and_download_excel(driver, company_name, download_dir)
        try:
            error_message_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*//*[contains(text(), "No details found for this criteria. Please enter valid Establishment name or code number .")]'))
            )
            if "No details found for this criteria" in error_message_element.text:
                return render(request, "home.html", {
                    "error": f"No details found for '{company_name}'. Please try again with a valid name.",
                    "success": False
                })
        except TimeoutException:
            pass  # No error message found, proceed

        # Further processing
        if not file_path or not os.path.exists(file_path):
            return render(request, "home.html", {"error": "No valid CSV file found.", "success": False})

        df = read_csv_file(file_path)
        if df is None or df.empty:
            return render(request, "home.html", {"error": "No records found for the specified company.", "success": False})

        conn = create_or_connect_database("company_pf_details.db")
        write_to_table(conn, df, "company_data")
        conn.close()

        return render(request, "home.html", {"success": True, "show_table_link": True})
    except Exception as e:
        return render(request, "home.html", {"error": f"An error occurred: {e}", "success": False})
    finally:
        if driver:
            driver.quit()  # Safely quit the driver

@app.route("/show_table")
def show_table(request):
    """Display the table with checkboxes and handle form submissions."""
    if request.method == "POST":
        selected_companies = request.POST.getlist("selected_companies")
        selected_data = []
        conn = create_or_connect_database("company_pf_details.db")
        print("selected_companies", selected_companies)
        cursor = conn.cursor()
        for est_id in selected_companies:
            cursor.execute("SELECT establishment_name FROM company_data WHERE establishment_id=?", (est_id,))
            est_name = cursor.fetchone()[0]
            selected_data.append({"establishment_id": est_id, "establishment_name": est_name})
        conn.close()
        
        # Pass the selected companies to the final scraper
        for data in selected_data:
            epfs_scraper().scrape_data(company_name=data["establishment_name"], est_id=data["establishment_id"], rename=True)
            time.sleep(5)
        print("here0")
        # Save to backend and create a new table with the name of payment_detail
        for data in selected_data:
            company_name = data["establishment_name"]
            est_id = data["establishment_id"]
            download_dir2 = os.path.join(os.getcwd(), "data")
            os.makedirs(download_dir2, exist_ok=True)  # Ensure directory exists

            driver = None
            try:
                company_name=company_name.replace(" ","_")
                file_path2 = f"data/{company_name}.xlsx"
                check_excel_file(file_path2)
                file_path2 = file_path2.replace(".xlsx",".csv")
                print("here1")
                print(file_path2)
                df2 = read_csv_file2(file_path2, company_name)
                if df2 is None:
                    return render(request, "home.html", {"error": "No records available for the organization ", "success": False})
                # cant read
                print("workbook", df2.head())
                print("here2")
                # Step 2: Ensure the file exists or fetch the latest one
                if not os.path.exists(file_path2):
                    file_path2 = get_latest_file(download_dir2, "*.csv")
                    if not file_path2:
                        return render(request, "home.html", {"error": "No valid CSV file found.", "success": False})

                # Step 3: Read the downloaded CSV file
                if df2 is None:
                    return render(request, "home.html", {"error": "Failed to read the downloaded CSV file.", "success": False})

                # Step 4: Connect to the SQLite database
                conn = create_or_connect_database("company_pf_details.db")
                if conn is None:
                    return render(request, "home.html", {"error": "Database connection failed.", "success": False})

                # Step 5: Write the data to the database
                write_to_table(conn, df2, "payment_detail")

                # Close the database connection
                conn.close()
                if os.path.exists(file_path2):
                    os.remove(file_path2)
                    print(f"Removed file: {file_path2}")
                xlsx_file_path = file_path2.replace(".csv", ".xlsx")
                if os.path.exists(xlsx_file_path):
                    os.remove(xlsx_file_path)
                    print(f"Removed file: {xlsx_file_path}")

            except Exception as e:
                return render(request, "home.html", {"error": f"An error occurred: {e}", "success": False})
            finally:
                if driver:
                    driver.quit()  # Safely quit the driver
        
        return redirect("/payment_details")

    # Read the DataFrame from `company_data` table
    conn = create_or_connect_database("company_pf_details.db")
    df = pd.read_sql_query("SELECT * FROM company_data", conn)
    conn.close()

    # Convert DataFrame rows to a list of lists and column names to a list
    data = df.values.tolist()  # Each row as a list
    columns = df.columns.tolist()  # List of column names

    return render(request, "show_table.html", {"data": data, "columns": columns})

@app.route("/payment_details")
def payment_details(request):
    """Display the payment details."""
    conn = create_or_connect_database("company_pf_details.db")
    df = pd.read_sql_query("SELECT * FROM payment_detail", conn)
    conn.close()

    # Convert DataFrame rows to a list of lists and column names to a list
    data = df.values.tolist()  # Each row as a list
    columns = df.columns.tolist()  # List of column names

    return render(request, "payment_details.html", {"data": data, "columns": columns})

if __name__ == "__main__":
  webbrowser.open("http://localhost:8004")
  app.run(host="0.0.0.0:8004")