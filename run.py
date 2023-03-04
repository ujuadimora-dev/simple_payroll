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
SHEET = GSPREAD_CLIENT.open("simple_payrolls").sheet1
#sheet = client.open('Employee Data').sheet1


def employee_data():
    global name
    """
    Get the employee details vie the Terminal and add the
     employee data to the google spreadheet
    """
    print("*********************************************************************************************")
    print("***************Welcome tho the Simple__payroll automation************************************")
    print("*********This program help you to enter Employee Data vie terminal, add record to ***********")
    print ("the spreadsheet and calculate and print the netpay for each employee for a week( 5 working days)")
    print("*************************************************************************************************")
    #answer = input("Do you want to enter employee data? (yes/no/end): ")
    employees = []
    while True:
        id = input("Enter employee id: ")
        if not id.isalnum():
            print("Invalid id. Please enter a valid id containing only letters.")
            continue
        name = input("Enter employee name: ")
        if not name.isalpha():
            print("Invalid name. Please enter a valid name containing only letters.")
            continue
        age = input("Enter employee age: ")
        if not age.isdigit() or int(age) < 18 or int(age) > 100:
            print("Invalid age. Please enter a valid age between 18 and 100.")
            continue
        department = input("Enter employee department: ")
        if not department.isalpha():
            print("Invalid department. Please enter a valid position containing only letters.")
            continue
        salary = input("Enter employee Basic Salary: ")
        if not salary.isdigit():
            print("Invalid salary. Please enter a valid salary containing only numbers.")
            continue
        employees.append({"id": id,"name": name, "age": age, "department": department})

        # add the employ detail to the spreed sheet
        print("updating  employee record... \n")
        SHEET.append_row([id, name, age, department, salary])
        print("Employee Records  update sucessfull \n")
        another_employee = input("Do you want to enter another employee? (yes/no/end): \n")
        if  another_employee.lower() == "end":
            exit()
        if another_employee.lower() == "no":
            break
    return employees

employees = employee_data()
print(employees)
 

def hour_work_week():
    """
    this is to calcualte the over time per week
    """
    print("*******************************************************************")
    print("This section is to calculate actual salary of an employer per week")
    print("******************************************************************")
   
    global total_hours
    print('Enter the name of the employee to get Net salary for the week')
    global name
    name = input("Enter employee name: ")
    while True:
        print(f"Please enter one week hours for {name}.")
        print("numbers of hours puting must be sparated by commas")
        print("(Example: 6,5,0,6,5)\n")

        data_str = input("Enter your data here: ")

        hours_worked = data_str.split(",")

        if valid_hours(hours_worked):
            print("Hours is valid!")
            break

    print (hours_worked)
    sum = 0
    for i in range(5):
        sum += int(hours_worked[i])
        # Print the sum
    print(f"The sum of hours worked for 5 working days(a week) for {name}:", sum)
    total_hours = sum
    
    

def valid_hours(hours_worked):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in hours_worked]
        if len(hours_worked) != 5:
            raise ValueError(
                f"Exactly 5 values required, you provided {len(hours_worked)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

#print(hours_worked)
#hour_work_week()
#valid_hours(values)
#print(hours_worked)
#hour_work_week()   
hourly_rate = float(input("Enter hourly rate: "))

def overtime(total_hours, hourly_rate):
    """
    this is to calcualte the over time per week
    """
    # assume the regular work hours and maximum hours per day

    employee_regular_hours = 40
    max_hours_per_day = 8
    hourly_rate = 10
    total_hours = f"{total_hours}" 
    


    if int(total_hours) > 40:
        overtime_hours =  int(total_hours) - 40
        overtime_pay = overtime_hours * hourly_rate * 1.5
    else:
        overtime_pay = 0
    return overtime_pay

def net_pay( total_hours, hourly_rate):
    hourly_rate = 10
    regular_pay = total_hours * hourly_rate
    overtime_pay = overtime(total_hours, hourly_rate)
    total_pay = regular_pay + overtime_pay
    print(f"Regular pay: {regular_pay}")
    print(f"Overtime pay: {overtime_pay}")
    print(f"Total pay: {total_pay}")
    response = input("Do you want to calculate another paycheck? (y/n): ")
    if response.lower() == "y":
        hourly_rate = float(input("Enter hourly rate: "))
        hour_work_week()
        #name = input("Enter employee name: ")
       #hour_work_week():
        #total_hours = float(input(f"Enter hours worked for {name}: "))
        #hourly_rate = float(input("Enter hourly rate: "))
        overtime(total_hours,hourly_rate)
        net_pay( total_hours, hourly_rate)
    else:
        print("Goodbye!")



hour_work_week()   
overtime(total_hours,hourly_rate)
net_pay( total_hours,hourly_rate)
