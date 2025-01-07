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
from db_func import read_excel_file, create_or_connect_database, write_to_table  # Import functions from Backfunc.py


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

def renameMostRecentFile(
    new_name: str,
    directory: str,
 
):
    """
    Method to rename the most recent file in the specified directory.

    Input:
        new_name (str): The new name for the file.
        directory (str): The directory where the file is located.
        dataClass (scrapped_data, optional): The data class structure. Defaults to scrapped_data.

    Output:
        None
    """
    try:
        # Get list of files in the directory sorted by creation time
        files = sorted(os.listdir(directory), key=lambda x: os.path.getctime(os.path.join(directory, x)))
        
        if files:  # Check if there are any files in the directory
            most_recent_file = files[-1]  # Get the most recent file
            old_path = os.path.join(directory, most_recent_file)
            new_path = os.path.join(directory, f'{new_name}')
            print(f"OLD PATH:{old_path}")
            print(f"new_path{new_path}")
            os.rename(old_path, new_path)
            print(f"File '{most_recent_file}' renamed to '{new_name}' successfully.")

        else:
            print(f"No files found in directory '{directory}'.")
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
    except FileExistsError:
        print(f"Error: File '{new_name}' already exists.")
    return new_path

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
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="example_wrapper"]/div[1]/a/span'))
            )
            driver.find_element(By.XPATH, '//*[@id="example_wrapper"]/div[1]/a/span').click()
            time.sleep(5)
            retry = False
        except TimeoutException:
            print("Invalid CAPTCHA or Excel button not clickable. Retrying...")
    print(f"download_dir-{download_dir}")
    print(f"file_name-{file_name}") 
    renamed_file = renameMostRecentFile(file_name, download_dir)
    print(f"renamed_file-{renamed_file}")
    return renamed_file   