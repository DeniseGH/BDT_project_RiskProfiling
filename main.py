from setting_database import setup_database
from loan_records import insert_loan_records
from fully_paid import insert_fully_paid
from ongoing_records import create_ongoing_table

# configuring database
setup_database()

# creating records and adding to "loan_records" table
insert_loan_records(1000)

# extracting fully paid records from "loan_records" table
insert_fully_paid()

# creating records and adding to "ongoing" table
create_ongoing_table(100)


