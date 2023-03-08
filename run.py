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
#This authenticate and authorize access to Google Cloud APIs.
CREDS = Credentials.from_service_account_info(creds)

SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# Connect to the Google Sheets API
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
 #Open the spreadsheet
SHEET = GSPREAD_CLIENT.open("simple_payrolls").sheet1
#sheet = client.open('Employee Data').sheet1



print("***************************************************************")
print("***********Welcome to the Simple__payroll automation***********")
print(" ***********It has two section: Section1 and section2***********")
print("***Section 1: This program help you to enter Employese Data*****")
print("******** vie terminal, add record to the spreadsheet ***********")
print("***Section 2: calculate, overtime, Deductions and Net pay*******")
print("**print them for each employee for a week(5 working days)*******")
print("****************************************************************")


def employee_data():
    
    """
    Get the employees details vie the Terminal and add the
    employees data to the google spreadheet
    """
    print(" Welcome to section 1")
    employees = []
    while True:
        id = input("Enter employee id: ")
        if not id.isalnum():
            print("Invalid id. Please enter a valid id containing only letters and numbers.")
            id = input(" Re-enter employee id: ")


        name = input("Enter employee name: ")
        if not name.isalpha():
            print("Invalid name. Please enter a valid name containing only letters.")
            name = input("Re-enter employee name: ")

        age = input("Enter employee age: ")
        if not age.isdigit() or int(age) < 18 or int(age) > 100:
            print("Invalid age. Please enter a valid age between 18 and 100.")
            age = input("Re-enter employee age: ")
         
        department = input("Enter employee department: ")
        if not department.isalpha():
            print("Invalid department. Please enter a valid position containing only letters.")
            department = input("Re-enter employee department: ")
          
        salary = input("Enter employee Basic Salary: ")
        if not salary.isdigit():
            print("Invalid salary. Please enter a valid salary containing only numbers.")
            salary = input("Re-enter employee Basic Salary: ")
           
        employees.append({"id": id,"name": name, "age": age, "department": department})

        # add the employ detail to the spreed sheet
        print("updating  employee record... \n")
        SHEET.append_row([id, name, age, department, salary])
        print("Employee Records added sucessfull \n")

        another_employee = input("Do you want to enter another employee? (yes/no/end): \n")

        if another_employee.lower() == "no":
            
            break
        elif another_employee.lower() == "end":
             print("Program ended! Thanks for using our Program.")
             exit()
        else:
            continue

    return employees
#employees = employee_data()


def hour_work_week():
    """
    This inputs the 5 days week hours and calculates the over 
    time per week
    """
    global name
    name = input("Enter employee name: ")
    while True:
        print(f"Please enter one week hours for {name}.")
        print("Numbers of hours puting must be separated by commas")
        print("(Example: 6,5,0,6,5)\n")

        hour_str = input("Enter hours here: ")
        hours_worked = hour_str.split(",")

        if valid_hours(hours_worked):
            print("Hours entered are valid!")
            break

    print(hours_worked)
    total_hours = sum([int(hour) for hour in hours_worked])
    print(f"The sum of hours worked for 5 working days (a week) for {name}: {total_hours}")

    hourly_rate = float(input("Enter hourly1 rate: "))
    net_pay(total_hours, hourly_rate)

def valid_hours(hours_worked):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 5 values.
    """
    try:
        hours_int = [int(value) for value in hours_worked]
        if len(hours_int) != 5:
            raise ValueError(
                f"Exactly 5 values required, you provided {len(hours_int)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def net_pay(total_hours, hourly_rate):
    """
    This function calculates the overtime, regular pay,
    and total net pay of an employee
    """
    # assume maximum hours per week is 40
    employee_regular_hours = 40
    over_time_hr = total_hours - employee_regular_hours
    regular_pay = employee_regular_hours * hourly_rate
    
    # This gets the total deduction that must be deducted from the regular pay;
    health_insurance = 0.05 * regular_pay
    social_maintance_fees = 0.03 * regular_pay
    total_deduction = round(float(health_insurance + social_maintance_fees))
    total_pay = regular_pay - total_deduction

    

    # This check if employee has worked overtime or not.
    if   total_hours <= 40:
        print(f"     PayRoll Information for {name}")
        print("**************************************")
        print(f"Pay rate   ${hourly_rate }")
        print(f"Employee Regular Hours {employee_regular_hours }")
        print("overTime Hours:     0")
        print(" Over Time pay:   $0.00")
        print(f"Basic pay:    ${regular_pay}")
        print(f"Total Deduction: ${total_deduction}")
        print("**********************************")
        print(f"TotalNet Pay:  ${total_pay}")
    else:
        total_hours > 40
        over_time_hr =  total_hours - 40
        overtime_pay = over_time_hr * hourly_rate * 1.5
        
        print(f"     PayRoll Information for {name}")
        print("**************************************")
        print(f"Pay rate:   ${hourly_rate }")
        print(f"Employee Regular Hours:{employee_regular_hours }")
        print(f"over time hour:{over_time_hr}")
        print(f"Overtime pay: ${overtime_pay}")
        print(f"Basic pay:    ${regular_pay}")
        print(f"Total Deduction: $ {total_deduction}")
        print("***************************************")
        print(f"TotalNet Pay:    ${total_pay}")

    # This is asking the user if they want to calculate another netpay. 
    response = input("Do you want to calculate another paycheck? (yes/no): ")
    if response.lower() == "yes":
        hour_work_week()
        total_hours = int(total_hours)
        net_pay(total_hours, hourly_rate)
        
    else:
        print("Thanks for using our Program, See you again!")
        exit()

    return net_pay(total_hours, hourly_rate)

while True:
    # Display menu options
    print("Choose an option:")
    print("1. Enter employee data")
    print("2. Calculate net pay")
    print("3. Quit")

    # Get user choice
    choice = input("Enter your choice (1-3): ")

    # Execute selected function
    if choice == "1":
        employees = employee_data()
    elif choice == "2":
       #hour_rate()
        #hour_work_week()
        #hourly_rate = float(input("Enter hourly2 rate: "))
        hour_work_week()
        total_hours = int(total_hours)
        net_pay(total_hours , hourly_rate)
    elif choice == "3":
        break
    else:
        print("Invalid choice. Please try again.")
