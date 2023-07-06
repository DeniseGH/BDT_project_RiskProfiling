from classes import Loan
import random
from SQL_manager import DatabaseConnector


def create_ongoing_loans(number_el):
    """
    :param number_el: decides how many rows add to the "Ongoing Loan" table
    :return:
    """

    db = DatabaseConnector('CREDIT_RECORDS.db')

    for _ in range(number_el):
        loan = Loan.create_random_loan(Loan)
        # Setting standards for ongoing records to be truthful
        delay = random.randint(0, 1)
        loan_status = "Ongoing"
        suffering = "No"
        column_names= db.get_column_names("ongoing")
        # Construct the INSERT query dynamically using column_names
        query = "INSERT INTO ongoing ({}) VALUES ({})".format(
            ", ".join(column_names),
            ", ".join(["?" for _ in column_names])
        )

        # Prepare the values for insertion
        values = (
            loan.client.customer_id, loan.loan_id, loan.client.name, loan.client.age, loan.client.education,
            loan.client.income, delay, suffering, loan.client.coappl, loan.client.dep, loan.client.saves,
            loan.client.coappinc, loan.amount, loan.purpose, loan.term, loan_status
        )

        # Execute the query with the prepared values
        db.execute_query(query, values)

    db.close()
