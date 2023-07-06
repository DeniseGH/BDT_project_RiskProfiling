from classes import Loan
from functions import monthly_dept, complex_income
from SQL_manager import DatabaseConnector


def insert_loan_records(number_el):
    """
    :param Loan: creates loan records to be added to the namesake table
    :param number_el: decides how many records create
    """
    db = DatabaseConnector('CREDIT_RECORDS.db')

    for _ in range(number_el):
        loan = Loan.create_random_loan(Loan)

        column_names = db.get_column_names("loan_records")
        # Construct the INSERT query dynamically using column_names
        query = "INSERT INTO loan_records ({}) VALUES ({})".format(
            ", ".join(column_names),
            ", ".join(["?" for _ in column_names])
        )

        # Prepare the values for insertion
        values = (
            loan.client.customer_id, loan.loan_id, loan.client.name, loan.client.age, loan.client.education,
            loan.client.income, loan.client.delay, loan.client.suffering, loan.client.coappl, loan.client.dep, loan.client.saves,
            loan.client.coappinc, loan.amount, loan.purpose, loan.term, loan.status
        )

        # Execute the query with the prepared values
        db.execute_query(query, values)

        tot_inc = complex_income(loan.client.income, loan.client.coappinc, loan.client.dep)
        mon_dep = monthly_dept(tot_inc)
        if loan.client.delay >= 2 or loan.client.suffering == "Yes" or loan.client.saves < 2 * mon_dep:
            db.execute_query(
                "UPDATE loan_records SET Status = ? WHERE CRIF_delay = ? AND CR_suffering = ? and Savings = ?",
                ("Declined", loan.client.delay, loan.client.suffering, loan.client.saves))

    db.close()
