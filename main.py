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
from forms import CompanySearchForm
from django.db import models


from scrapper_final import epfs_scraper
from db_func import read_csv_file, write_to_company_data, write_to_payment_detail, read_csv_file2
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

@app.admin
class Company_Data(models.Model):
    establishment_id = models.CharField(max_length=100, primary_key=True)
    establishment_name = models.CharField(max_length=255)
    address = models.TextField()
    office_name = models.CharField(max_length=100)

@app.admin
class Payment_Detail(models.Model):
    company_name = models.CharField(max_length=255)
    trrn = models.BigIntegerField()
    date_of_credit = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    wage_month = models.CharField(max_length=50)
    no_of_employee = models.IntegerField()
    ecr = models.CharField(max_length=10)

@app.route("/")
def home(request):
    return render(request, 'home.html')

@app.route("/search")
def search(request):
    form = CompanySearchForm(request.GET or None)

    if not form.is_valid():
        return render(request, "home.html", {"form": form, "error": form.errors, "success": False})

    company_name = form.cleaned_data["company_name"]
    download_dir = os.path.join(os.getcwd(), "CompanyList")
    os.makedirs(download_dir, exist_ok=True)

    driver = None
    try:
        driver = setup_driver(download_dir)
        file_path = search_and_download_excel(driver, company_name, download_dir)

        if file_path == "INVALID_COMPANY":
            return render(
                request,
                "home.html",
                {
                    "form": form,
                    "error": f"No details found for '{company_name}'. Please try a valid Establishment name or code number.",
                    "success": False,
                },
            )

        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError("No valid CSV file found.")

        # Process the file and write to the database
        df = read_csv_file(file_path)
        if df.empty:
            raise ValueError("No records found in the file.")
        print("this is the data->",df.head())
        write_to_company_data(df, Company_Data)
        print("this is the data2->",df.head())

        data = Company_Data.objects.all()
        print("data--?:",data) # This will print a queryset of the rows
        

        return render(request, "home.html", {"form": form, "success": True, "show_table_link": True})

    except Exception as e:
        return render(request, "home.html", {"form": form, "error": f"An error occurred: {e}", "success": False})

    finally:
        if driver:
            driver.quit()

@app.route("/show_table")
def show_table(request):
    """Display the table with checkboxes and handle form submissions."""
    if request.method == "POST":
        selected_companies = request.GET.getlist("selected_companies")
        selected_data = Company_Data.objects.filter(establishment_id=selected_companies)
        
        for data in selected_data:
            epfs_scraper().scrape_data(company_name=data.establishment_name, est_id=data.establishment_id, rename=True)
            time.sleep(5)

        for data in selected_data:
            company_name = data.establishment_name
            est_id = data.establishment_id
            download_dir2 = os.path.join(os.getcwd(), "data")
            os.makedirs(download_dir2, exist_ok=True)

            driver = None
            try:
                company_name=company_name.replace(" ","_")
                file_path2 = f"data/{company_name}.xlsx"
                check_excel_file(file_path2)
                file_path2 = file_path2.replace(".xlsx",".csv")
                print("here1")
                print(file_path2)
                df2 = read_csv_file2(file_path2, company_name)
                print(df2.head())
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

                # Step 4: Write the data to the database
                print(df2.head())
                write_to_payment_detail(df2, Payment_Detail)

                # Remove the file after saving to the database
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

    data=Company_Data.objects.all()
    
    data_list=list(data.values())
    columns=[field.name for field in Company_Data._meta.fields]

   
    return render(request, "show_table.html", {"data": data_list, "columns": columns})

@app.route("/payment_details")
def payment_details(request):
    """Display the payment details."""
    data=Payment_Detail.objects.all()

    data_list=list(data.values())
    columns=[field.name for field in Payment_Detail._meta.fields]

    return render(request, "payment_details.html", {"data": data_list, "columns": columns})

if __name__ == "__main__":
  webbrowser.open("http://localhost:8004")
  app.run(host="0.0.0.0:8004")