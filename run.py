import gspread
from google.oauth2.service_account import Credentials
import json

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





def get_employee_data():
    """
    Get or input user details.
    We run a for loop to collect as many as possible data of emplyees 
    via the terminal, 
    """

    employees = []
    for i in range(1):
        print(f"Enter details for Employee {i+1}: \n")
        employeeid = input("ID: \n")
        name = input("Name:  \n")
        age = int(input("Age:  \n"))
        department = input("Dept:  \n")
        salary = float(input("Salary:  \n"))
        employee = {'Name': name, 'Age': age, 'Salary': salary}
        employees.append(employee)
    print(employee) 

get_employee_data()  



