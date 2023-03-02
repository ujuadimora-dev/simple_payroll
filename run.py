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
        another_employee = input("Do you want to enter another employee? (yes/no): ")
        if another_employee.lower() == "no":
            break
    return employees

employees = employee_data()
print(employees)
 

def cal_over_time():
    """
    this is to calcualte the over time per week
    """
    
    
    print('Enter the name of the employee to ge Net salary for the week')
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






# define a function to add employee data to the spreadsheet
#def add_employee_data():
 #   name = input('Enter employee name: ')
  #  age = input('Enter employee age: ')
   # position = input('Enter employee position: ')
    #salary = input('Enter employee salary: ')
    
    # add the employee data to the spreadsheet
    #SHEET.append_row([name, age, position, salary])
    
    # ask the user if they want to continue adding data
    #answer = input('Do you want to add more data? (y/n) ')
    #if answer == 'y':
        #add_employee_data()
    #else:
        ## call another function or exit the program here
        #print('Program completed.')

# call the function to add employee data
#add_employee_data()