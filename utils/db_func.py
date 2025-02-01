import csv
import pandas as pd
import sqlite3
from datetime import datetime


def read_csv_file(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            # check
            print(f"Column names in CSV: {reader.fieldnames}")

            # csv col to keys ma krdiya
            records = []
            for row in reader:
                row.pop('Action', None)
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


def write_to_company_data(records, Company_Data):
    try:
        for record in records:
            Company_Data.objects.create(
                establishment_id=record['establishment_id'],
                establishment_name=record['establishment_name'],
                address=record['address'],
                office_name=record['office_name']
            )
        print("Data written to 'company_data' table successfully.")
    except Exception as e:
        print(f"Error writing to 'company_data' table: {e}")


def read_csv_file2(file_path, company_name):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            print(f"Column names in CSV: {reader.fieldnames}")

            records = []
            for row in reader:
                # convert doc format from 20-JAN-2017 20:29:26 to YYYY-MM-DD HH:MM:SS 
                try:
                    formatted_date = datetime.strptime(
                        row['Date Of Credit'], "%d-%b-%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    formatted_date = None  # handle invalid date formats

                records.append({
                    'company_name': company_name,
                    'trrn': row['TRRN'],
                    'date_of_credit': formatted_date,  # use converted date format
                    'amount': row['Amount'],
                    'wage_month': row['Wage Month'],
                    'no_of_employee': row['No. of Employee'],
                    'ecr': row['ECR']
                })
            return records
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []


def write_to_payment_detail(records, Payment_Detail):
    try:
        for record in records:
            Payment_Detail.objects.create(
                company_name=record['company_name'],
                trrn=record['trrn'],
                date_of_credit=record['date_of_credit'],
                amount=record['amount'],
                wage_month=record['wage_month'],
                no_of_employee=record['no_of_employee'],
                ecr=record['ecr']
            )
        print("Data written to 'payment_detail' table successfully.")
    except Exception as e:
        print(f"Error writing to 'payment_detail' table: {e}")
