from Ongoing_loans.analyzing_transactions import create_directory_path, find_json, check_loan_ids, \
    get_first_day_of_next_month
from Ongoing_loans.initializing_synthetic_payments_records import initialize_payment_redis
from Ongoing_loans.redis_manager import RedisManager
from Ongoing_loans.spark import update_json_file
from Ongoing_loans.transaction import _deserialize_transactions
from SQL_manager import DatabaseConnector

print("-------- You started your simulation ! -------- ")

# Connect to Redis
r = RedisManager().get_instance()

# Connect to the database in SQL
db = DatabaseConnector("CREDIT_RECORDS.db")

# Execute the SQL query to fetch loan_ids from the ongoing_records table
db.execute_query('SELECT loan_id FROM ongoing')

# Fetch all the loan_ids from the result set
loan_ids = db.fetchall()
db.close()

# Create a list of loan ids
loan_ids = [loan_id[0] for loan_id in loan_ids]

# It initializes the payment records using Redis
initialize_payment_redis(loan_ids, r)

print("-----------------")

# The date you want to start your simulation
year = input("Which year do you want to start your simulation? format (YYYY) ")
month = input("Which month do you want to start your simulation? (format MM) ")

date = year+"/"+month+"/01"

print("-----------------")

print(" ---- You chose to start your simulation the: ", date)
print("Transaction will be simulated starting from the 30 days before you selected date")

# The name we want to assign to the main directory (the year will be concatenated)
json_file_path = "loan_repayments_transactions"

print(" ---- The directory will have the following name: ", json_file_path, "_",year)

while True:
    number_of_month = input("How many months do you want to simulate? ")
    if number_of_month.isdigit():
        number_of_month = int(number_of_month)
        break
    else:
        print("Invalid input. Please enter a valid integer for the number of months you would like.")


for _ in range(0, number_of_month):
    # Update the JSON file creating 2 directories:
    update_json_file(json_file_path, date, r)

    # The 2 directory paths of the folders
    directory_path = create_directory_path(date)

    # json data of the transactions on time
    json_data = find_json(directory_path)

    # json data deserialized in a list of transactions
    transactions_list = _deserialize_transactions(json_data)

    check_loan_ids(transactions_list, r)

    date = str(get_first_day_of_next_month(date))


# It removes the information from Redis to get ready for another simulation
r.flushall()
print("Redis is now flushed, you are ready to proceed with another simulation")

