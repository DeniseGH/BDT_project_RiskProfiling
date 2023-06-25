import random

from Ongoing_loans.synthetic_data_transactions import generate_monthly_payment
from SQL_manager import DatabaseConnector
from functions import complex_income, monthly_dept, duration, interest_rate


def initialize_payment_redis(loan_ids: list, r):
    """
    param loan_ids: A list of loan IDs from the "ongoing" SQL table.
    param r: The redis connector.
    :return: None
    """
    db = DatabaseConnector("CREDIT_RECORDS.db")

    # The for loop iterates over each loan ID in the provided list and uses the hset function to set the "months_left"
    # and "late_transactions" fields in Redis with randomly generated values.
    for loan_id in loan_ids:

        # Execute the queries
        amount = db.execute_query_by_loan_id(loan_id, "ongoing", "Amount")
        purpose = db.execute_query_by_loan_id(loan_id, "ongoing", "Purpose")
        int_rate = interest_rate(purpose)
        income = db.execute_query_by_loan_id(loan_id, "ongoing", "Income")
        coApp_Income = db.execute_query_by_loan_id(loan_id, "ongoing", "CoApp_Income")
        dependents_No = db.execute_query_by_loan_id(loan_id, "ongoing", "Dependents_No")
        dept = monthly_dept(complex_income(income, coApp_Income, dependents_No))

        # set the duration up to the overall duration of the loan
        r.hset(loan_id, "months_left", random.randint(1, duration(amount, int_rate, dept)))
        r.hset(loan_id, "late_transactions", random.randint(0, 1))

    # Close the database connection
    db.close()
    # The print statement displays the number of payment records that have been initialized in Redis.
    print(len(loan_ids), " payments records from the ongoing SQL table have been initialized in Redis.")


