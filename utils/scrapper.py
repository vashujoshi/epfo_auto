import os
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
import easyocr
import time
import pandas as pd
from xlsx2csv import Xlsx2csv

# URL for EPFO search page
EPFO_SEARCH_URL = "https://unifiedportal-emp.epfindia.gov.in/publicPortal/no-auth/misReport/home/loadEstSearchHome"

def setup_driver(download_dir):
    """Set up the Selenium WebDriver with download directory options."""
    options = Options()
    prefs = {"download.default_directory": download_dir}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    return driver

def solve_captcha(driver):
    """Solve CAPTCHA using EasyOCR."""
    reader = easyocr.Reader(lang_list=["en"], gpu=True)
    captcha_image = driver.find_element(By.ID, "capImg").screenshot_as_png
    captcha_img = Image.open(BytesIO(captcha_image))

    # OCR to extract text
    extracted_text = reader.readtext(np.array(captcha_img), detail=0, paragraph=True)
    if not extracted_text:
        return None

    # Process the extracted CAPTCHA text
    captcha_text = extracted_text[0]
    captcha_text = "".join(captcha_text.split(" ")).upper()  # Remove spaces and convert to uppercase
    captcha_text = captcha_text.replace("$", "S").replace("€", "E").replace(")", "J") # Replace ambiguous characters

    return captcha_text

def renameMostRecentFile(new_name: str, directory: str):
    """
    Method to rename the most recent file in the specified directory.

    Input:
        new_name (str): The new name for the file.
        directory (str): The directory where the file is located.

    Output:
        str: The new file path.
    """
    try:
        # Get list of files in the directory sorted by creation time
        files = sorted(os.listdir(directory), key=lambda x: os.path.getctime(os.path.join(directory, x)))
        
        if files:  # Check if there are any files in the directory
            most_recent_file = files[-1]  # Get the most recent file
            old_path = os.path.join(directory, most_recent_file)
            new_path = os.path.join(directory, f'{new_name}.csv')
            print(f"OLD PATH:{old_path}")
            print(f"new_path:{new_path}")
            Xlsx2csv(old_path, outputencoding="utf-8").convert(new_path)
            os.remove(old_path)
            print(f"File '{most_recent_file}' converted to '{new_name}.csv' successfully.")
            return new_path
        else:
            print(f"No files found in directory '{directory}'.")
            return None
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return None
    except FileExistsError:
        print(f"Error: File '{new_name}.csv' already exists.")
        return None

def read_csv_with_fallback(file_path):
    """
    Read a CSV file.

    Input:
        file_path (str): The path to the CSV file.

    Output:
        pd.DataFrame: The data read from the file.
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Failed to read CSV file: {e}.")
        df = None
    return df

def search_and_download_excel(driver, company_name, download_dir):
    print(f"Downloading Excel file to directory: {download_dir}")
    """Search for the company and download the Excel file."""
    driver.get(EPFO_SEARCH_URL)
    time.sleep(2)

    os.makedirs(download_dir, exist_ok=True)
    file_name = os.path.join(download_dir, f"{company_name.replace(' ', '_')}.xlsx")

    if os.path.exists(file_name):
        return file_name

    retry = True
    while retry:
        driver.find_element(By.NAME, "estName").clear()
        driver.find_element(By.NAME, "estName").send_keys(company_name)

        captcha_text = solve_captcha(driver)
        if not captcha_text:
            driver.refresh()
            time.sleep(2)
            continue

        driver.find_element(By.NAME, "captcha").clear()
        driver.find_element(By.NAME, "captcha").send_keys(captcha_text)
        driver.find_element(By.NAME, "Search").click()

        try:
            # Check if the error message "No details found for this criteria" is displayed
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="tablecontainer"]/div'))
            )
            error_message = driver.find_element(By.XPATH, '//*[@id="tablecontainer"]/div').text
            print(f"Error1: {error_message}")
            if "No details found for this criteria. Please enter valid Establishment name or code number ." in error_message:
                print(f"Error2: {error_message}")
                return "INVALID_COMPANY"
        except TimeoutException:
            pass  # Proceed only if no error message is found

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="example_wrapper"]/div[1]/a/span'))
            )
            driver.find_element(By.XPATH, '//*[@id="example_wrapper"]/div[1]/a/span').click()
            time.sleep(5)
            retry = False
        except TimeoutException:
            print("Invalid CAPTCHA or Excel button not clickable. Retrying...")

    renamed_file = renameMostRecentFile(company_name.replace(' ', '_'), download_dir)
    return renamed_file



    