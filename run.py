import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import sys

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
    global name
    """
    Get the employee details vie the Terminal
    """
    print("Please enter Employee Details to update the Employees record \n")

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

#employee_data()

def update_employee_record(data):
    """
    update the emplyee record worksheet
    """
    print("updating  employee record... \n")

    employee_worksheet = SHEET.worksheet("employees")
    
    employee_worksheet.append_row(data_details)

    print("Employee Records  update sucessfull \n")

data_details= employee_data()

update_employee_record(data_details)




    

def cal_over_time():
    """
    this is to calcualte the over time per week
    """
    # assume the regular work hours and maximum hours per day
    
    employee_regular_hours = 40
    max_hours_per_day = 8


   # # Define the regular work hours and maximum hours per day
    global name
    name =  input('enter  employee Name \n ')
    #employee_regular_hours = 40
    #max_hours_per_day = 8

    # Calculate the total hours per week worked by the employee
    
    print(f"one week worked hours for {name}  \n")
    print("(Example: 6,5,0,6,5\n)")
    data_str = input(f"Enter worked hours  per week for {name}: \n")

    hours_worked = data_str.split(",")
    print(hours_worked)

    # Initialize a variable to hold the sum
    sum = 0

    # Iterate over the 5 elements of the array and add them to the sum
    for i in range(5):
        sum += int(hours_worked[i])

    # Print the sum
    print("The sum of hours worked for 5 working days(a week):", sum)
    total_hours = sum
    # Calculate the overtime hours
    global over_time
    over_time =  total_hours -  employee_regular_hours

    # Print the results of the overtime/undertime hours worked per week
    print("Total hours worked:", total_hours)
    print("Overtime hours:", over_time)
    #print("Overtime pay:", overtime_pay)

cal_over_time()


def cal_net_pay():
    basic_salary = float(input(f"enter basic Salary for {name} \n"))

    health_insurance = 0.05 * basic_salary
    social_maintance_fees = 0.03 * basic_salary
    total_deduction = float(health_insurance + social_maintance_fees)

    net_pay = int((basic_salary + over_time) - total_deduction)

    print(net_pay)

cal_net_pay()



#data_details= employee_data()

#update_employee_record(data_details)


    

    