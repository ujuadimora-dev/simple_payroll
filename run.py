import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

import json
import csv

# Define the scope of the Google Sheets API access
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Load the credentials from the JSON file
creds = json.load(open('creds.json'))

CREDS = Credentials.from_service_account_info(creds)

SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# Connect to the Google Sheets API
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
 #Open the spreadsheet
SHEET = GSPREAD_CLIENT.open("simple_payrolls")

def employee_data():
    """
    Get the employee details vie the Terminal
    """
    print("Please enter Employee Details to update the Record \n")

    id =  input('Enter the ID number of Employee  \n ')

    name =  input('Enter the name of  Employee  \n ')

    age = int(input('Enter  Employee Age \n '))

    department =  input('Enter  the  Employee Department \n ')

    salary = float(input('Enter  employee  Basic Salary(gross income) \n'))

    data_details = [id, name, age, department, salary]

    print(data_details)

    #data_str = input("enter employee detail here  \n")
    #print(f"the data provided is {data_str}")

    #empl_data =  data_details.split(",")
    #print(empl_data)

    #print(data_details)

employee_data()

