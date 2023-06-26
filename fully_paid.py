from classes import Fully_Paid
from SQL_manager import DatabaseConnector


def insert_fully_paid():
    """
    This function retrieves "Fully Paid" loans from the principle table and inserts into the namesake table "Fully Paid" loan records
    """
    db = DatabaseConnector('CREDIT_RECORDS.db')

    fp_loans = Fully_Paid.extract_fully_paid_loans()

    column_names = db.get_column_names("fully_paid")

    # Construct the INSERT query dynamically using column_names
    query = "INSERT INTO fully_paid ({}) VALUES ({})".format(
        ", ".join(column_names),
        ", ".join(["?" for _ in column_names])
    )

    for row in fp_loans:
        db.execute_query(query, row)

    db.close()


