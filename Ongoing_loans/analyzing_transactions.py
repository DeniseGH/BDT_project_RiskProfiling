import os
import datetime

from functions import duration, interest_rate, monthly_dept, complex_income, last_fee
from SQL_manager import DatabaseConnector


def find_json(directory_path):
    '''
    :param directory_path: path of the directory containing the json files produced by Spark
    :return: a list (of length equal to the number of JSON files in the directory) containing JSON data.
    '''
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

    json_data_list = []

    for json_file in json_files:
        with open(os.path.join(directory_path, json_file), 'r') as file:
            json_data = file.read()

        json_data_list.append(json_data)

    return json_data_list


def create_directory_path(date):
    '''
    :param date:
    :return: the path to get to the directory
    '''
    parts = date.split('/')
    return 'loan_repayments_transactions_' + parts[0] + '/' + parts[1] + '/' + parts[2]


def check_loan_ids(transactions, r):
    '''
    :param transactions: list of the transactions of the selected month
    '''
    transactions_list_ontime = []
    transactions_list_late =[]

    for transaction in transactions:
        day = int(transaction.day.split("/")[2])  # Extract the day part and convert it to an integer
        if day <= 27:
            transactions_list_ontime.append(transaction)
        else:
            transactions_list_late.append(transaction)

    loan_ids_ontime = set(transaction.loan_id for transaction in transactions_list_ontime)
    loan_ids_late = set(transaction.loan_id for transaction in transactions_list_late)


    for loan_id in loan_ids_ontime.union(loan_ids_late):

        months_left = int(r.hget(loan_id, "months_left"))

        if months_left > 1:
            r.hset(loan_id, "months_left", months_left - 1)
            if loan_id in loan_ids_late:
                late_transactions = int(r.hget(loan_id, "late_transactions"))
                r.hset(loan_id, "late_transactions", late_transactions + 1)
        else:
            cancel_loan(loan_id, r, int(r.hget(loan_id, "late_transactions")))



def cancel_loan(loan_id, r, late_transactions):
    '''
    :param loan_id: loan_id that needs to be cancelled from the ongoing
    :param r: redis connector
    '''

    # Connect to the SQLite database
    db = DatabaseConnector("CREDIT_RECORDS.db")

    # Execute the queries
    db.execute_query("SELECT * FROM ongoing WHERE loan_id = ?", (loan_id,))
    row = db.fetchone()

    lr_column_names = db.get_column_names("loan_records")

    # Construct the INSERT query dynamically using column_names
    lr_query = "INSERT INTO loan_records ({}) VALUES ({})".format(
        ", ".join(lr_column_names),
        ", ".join(["?" for _ in lr_column_names])
    )

    db.execute_query(lr_query, row)

    updated = "UPDATE loan_records SET Status = ?, CRIF_delay= ? WHERE Loan_ID = ?"
    db.execute_query(updated, ("Fully Paid", late_transactions, loan_id))

    loan_amount = db.execute_query_by_loan_id(loan_id, "ongoing", "Amount")

    income = db.execute_query_by_loan_id(loan_id, "ongoing", "Income")

    CoApp_Income = db.execute_query_by_loan_id(loan_id, "ongoing", "CoApp_Income")

    Dependents_No = db.execute_query_by_loan_id(loan_id, "ongoing", "Dependents_No")

    purpose_fp = db.execute_query_by_loan_id(loan_id, "ongoing", "Purpose")

    co = complex_income(income, CoApp_Income, Dependents_No)

    dept_mon = monthly_dept(co)

    rate_int = interest_rate(purpose_fp)

    dur_fp = duration(loan_amount, rate_int, dept_mon)

    delay_fp = late_transactions

    lf = last_fee(dur_fp, dept_mon, rate_int, loan_amount)

    fp_loan = [loan_id, loan_amount, dept_mon, rate_int, dur_fp, delay_fp, lf]

    fp_column_names = db.get_column_names("fully_paid")

    # Construct the INSERT query dynamically using column_names
    fp_query = "INSERT INTO fully_paid ({}) VALUES ({})".format(
        ", ".join(fp_column_names),
        ", ".join(["?" for _ in fp_column_names])
    )

    db.execute_query(fp_query,  fp_loan)

    deleted = "DELETE FROM ongoing WHERE loan_id = ?"
    db.execute_query(deleted, (loan_id,))

    # Close the database connection
    db.close()

    # Delete the loan from Redis
    r.delete(loan_id)
    print("Loan ID: ", loan_id, " has been fully repaid, you can now find it in the fully_paid and loan_reacords SQL table!")
    print("The laon has been removed from Redis and from the SQL ongoing table")


def get_first_day_of_next_month(date):
    '''
    :param date: takes a date in this format "%Y/%m/%d" with day 01
    :return: returns a date in this format "%Y/%m/%d" with day 01 and the following month
    '''
    # Parse the input date
    input_date = datetime.datetime.strptime(date, "%Y/%m/%d").date()

    # Get the year and month of the input date
    year = input_date.year
    month = input_date.month

    # Increment the month by 1
    if month == 12: # in case of December
        year += 1
        month = 1
    else:
        month += 1

    # Create a new date object for the first day of the next month
    first_day_of_next_month = datetime.date(year, month, 1)

    # Return the first day of the next month
    return first_day_of_next_month.strftime("%Y/%m/%d")

