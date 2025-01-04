import time
import glob
import os
from django.shortcuts import render
from nanodjango import Django
from scrapper import setup_driver, search_and_download_excel
from db_func import read_excel_file, create_or_connect_database, write_to_table

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

def get_latest_file(directory, extension="*.xlsx"):
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
    print(f"Download directory is: {download_dir}")
    os.makedirs(download_dir, exist_ok=True)  # Ensure directory exists

    driver = None
    try:
        # Step 1: Initialize the driver and download the file
        driver = setup_driver(download_dir)
        file_path = search_and_download_excel(driver, company_name, download_dir)

        # Step 2: Ensure the file exists or fetch the latest one
        if not os.path.exists(file_path):
            file_path = get_latest_file(download_dir, "*.xlsx")
            if not file_path:
                return render(request, "home.html", {"error": "No valid Excel file found.", "success": False})

        # Step 3: Read the downloaded Excel file
        df = read_excel_file(file_path)
        if df is None:
            return render(request, "home.html", {"error": "Failed to read the downloaded Excel file.", "success": False})

        # Step 4: Connect to the SQLite database
        conn = create_or_connect_database("pf_tracker.db")
        if conn is None:
            return render(request, "home.html", {"error": "Database connection failed.", "success": False})

        # Step 5: Write the data to the database
        write_to_table(conn, df, "company_data")

        # Close the database connection
        conn.close()

        return render(request, "home.html", {"success": True, "file_path": file_path})
    except Exception as e:
        return render(request, "home.html", {"error": f"An error occurred: {e}", "success": False})
    finally:
        if driver:
            driver.quit()  # Safely quit the driver

if __name__ == "__main__":
    app.run(host="0.0.0.0:8004")
