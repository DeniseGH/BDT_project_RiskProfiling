from setting_database import setup_database
from loan_records import insert_loan_records
from fully_paid import insert_fully_paid
from ongoing_records import create_ongoing_loans

# --- TUNING PARAMETERS
NUMBER_OF_RECORDS = 1000
NUMBER_OF_ONGOING_RECORDS = 100

# configuring database
setup_database()

# creating records and adding to "loan_records" table
insert_loan_records(NUMBER_OF_RECORDS)

# extracting fully paid records from "loan_records" table
insert_fully_paid()

# creating records and adding to "ongoing" table
create_ongoing_loans(NUMBER_OF_ONGOING_RECORDS)

print(NUMBER_OF_RECORDS, "number of records have been created in a SQL table")


