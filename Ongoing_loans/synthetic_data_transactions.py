import random
from datetime import datetime, timedelta

from functions import monthly_dept, random_ids, complex_income
from SQL_manager import DatabaseConnector


# Generate a random transaction amount
def generate_monthly_payment(loan_id):
    # Connect to the database
    db = DatabaseConnector("CREDIT_RECORDS.db")

    # Execute the queries
    income = db.execute_query_by_loan_id(loan_id, "ongoing", "Income")

    CoApp_Income = db.execute_query_by_loan_id(loan_id, "ongoing", "CoApp_Income")

    Dependents_No = db.execute_query_by_loan_id(loan_id, "ongoing", "Dependents_No")

    co = complex_income(income,CoApp_Income, Dependents_No)
    dept = monthly_dept(co)

    # Close the database connection
    db.close()

    return dept

# Generate a random timestamp for a given day
def generate_timestamp():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f" {hour:02d}:{minute:02d}:{second:02d}"


def generate_transactions_for_day(loan_ids: list, day: str):
    transactions = []

    # Calculate the end date
    end_date = datetime.strptime(day, "%Y/%m/%d")
    print("I am now simulating 1 month of transactions until " + str(end_date))

    for i in range(len(loan_ids)):
        # Generate a random date within the interval
        random_date = end_date - timedelta(days=random.randint(0, 30))

        loan_id = loan_ids[i]
        amount = generate_monthly_payment(loan_id)
        timestamp = generate_timestamp()
        customer_id = random_ids()
        transaction = {
            "customer_id": customer_id,
            "loan_id": loan_id,
            "amount": amount,
            "day": random_date.strftime("%Y/%m/%d"),
            "time": timestamp
        }
        transactions.append(transaction)

    return transactions








