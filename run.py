import json
import gspread
from google.oauth2.service_account import Credentials
import sys


# Define the scope of the Google Sheets API access
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

# Load the credentials from the JSON file
creds = json.load(open("creds.json"))
# This authenticate and authorize access to Google Cloud APIs.
CREDS = Credentials.from_service_account_info(creds)

SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# Connect to the Google Sheets API
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# Open the spreadsheet
SHEET = GSPREAD_CLIENT.open("simple_payrolls").sheet1
# sheet = client.open('Employee Data').sheet1

print("***************************************************************")
print("***********Welcome to the Simple__payroll automation***********")
print("***********It has two section: Section1 and section2***********")
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
    global name
    print(" Welcome to the Employee Record Update section ")
    print("*************************************************")
    employees = []
    while True:
        idn = input("Enter employee idn: ")
        if not idn.isalnum():
            print("Invalid id.enter a valid idn,letters/numbers only.")
            idn = input(" Re-enter employee idn: ")

        name = input("Enter employee name: ")
        if not name.isalpha():
            print("Invalid name. Please enter a valid name containing only")
            print(" letter and there will no space between.")
            name = input("Re-enter employee name: ")

        age = input("Enter employee age: ")
        if not age.isdigit() or int(age) < 18 or int(age) > 100:
            print("Invalid age. Please enter a valid age between 18 and 100.")
            age = input("Re-enter employee age: ")

        department = input("Enter employee department: ")
        if not department.isalpha():
            print("Invalid department. Please enter a valid position ")
            print("containing only letters and no space in between.")
            department = input("Re-enter employee department: ")

        salary = input("Enter employee Basic Salary:$  ")
        if not salary.isdigit():
            salary = input("Re-enter employee Basic Salary:  ")
            print("Invalid salary. A valid salary containing only number")

        employees.append(
            {"idn": idn, "name": name, "age": age, "department": department}
        )

        # add the employ detail to the spreed sheet
        print("updating  employee record... \n")
        SHEET.append_row([idn, name, age, department, salary])
        print("Employee Records added sucessfull \n")

        another_employee = input(" Add another employee?(yes/no/end): \n")

        if another_employee.lower() == "no":
            break
        elif another_employee.lower() == "end":
            print("Program ended! Thanks for using our Program.")
            sys.exit()
        else:
            continue

    return employees


def hour_work_week():
    """
    This inputs the 5 days week hours and calculates the over
    time per week
    """
    print("**************************************************")
    print("*************NetPay calculation Section***********")
    print("**************************************************")
    global name
    name = input("Enter employee name: ")
    while True:
        print(f"Please enter one week worked hours for {name}.")
        print("Numbers of hours puting must be separated by commas")
        print("(Example: 6,5,0,6,5)\n")
        hour_str = input("Enter hours here: ")
        hours_worked = hour_str.split(",")
        if valid_hours(hours_worked):
            print("Hours entered are valid!")
            break
    print(hours_worked)
    total_hours = sum([int(hour) for hour in hours_worked])
    print(f"Total hours worked 5 working days  for {name}: {total_hours}")

    # valiidate the hourly data
    hourly_rate = input("Enter hourly rate: ")
    hourly_rate = float(hourly_rate)
    if not isinstance(hourly_rate, float) or hourly_rate < 7.5 or hourly_rate > 18:
        print("Invalid hourly_rate.A valid hourly_rate between 7.5 and 18.")
        hourly_rate = float(input("Re-enter employee hourly_rate: "))
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
    except ValueError as error:
        print(f"Invalid data: {error}, please try again.\n")
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

    if total_hours <= 40:
        print(f"     Paycheck Information for {name}")
        print("**************************************")
        print(f"Pay rate   ${hourly_rate }")
        print(f"Employee Regular Hours: {employee_regular_hours }")
        print(f"Total hours worked per week: {total_hours}")
        print("overTime Hours:     0")
        print(" Over Time pay:   $0.00")
        print(f"Basic pay:    ${regular_pay}")
        print(f"Total Deduction: ${total_deduction}")
        print("**********************************")
        print(f"TotalNet Pay:  ${total_pay}")
    else:
        total_hours > 40
        over_time_hr = total_hours - 40
        overtime_pay = over_time_hr * hourly_rate * 1.5
        total_pay = (regular_pay - total_deduction) + overtime_pay

        print(f"     Paycheck Information for {name}")
        print("**************************************")
        print(f"Pay rate:   ${hourly_rate }")
        print(f"Employee Regular Hours: {employee_regular_hours }")
        print(f"Total hours worked per week: {total_hours}")
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
        empl_response = input("Would you like to Add employees ? (yes/no): ")
    if empl_response.lower() == "yes":
        # employees = employee_data()
        employee_data()
    else:
        print("End of the Program see you again!")
        sys.exit()


while True:
    # Display menu options
    print("Choose an option:")
    print("1. Do you what to add/update Employees Record?")
    print("2. Do you want to Calculate net pay for Employees?")
    print("3. Do you want to end the Program?")
    # Get user choice
    choice = input("Enter your choice (1-3): ")
    # Execute selected function
    if choice == "1":
        employees = employee_data()
    elif choice == "2":
        hour_work_week()
        net_pay(total_hours, hourly_rate)
    elif choice == "3":
        print(" End of the program, see you again")
        break

    else:
        print("Invalid choice. Please try again.")
