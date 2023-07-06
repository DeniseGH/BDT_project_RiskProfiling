from Ongoing_loans.synthetic_data_transactions import generate_transactions_for_day
from pyspark.sql import SparkSession

def update_json_file(json_file_path, day, r):
    """
    Update a JSON file with transactions data for a specific day.

    Args:
        json_file_path (str): Path to the JSON file.
        day (str): Day for which transactions are generated.
        r (redis): Redis connector.

    Returns:
        None
    """

    # Get the loan IDs from Redis
    loan_ids = []

    keys = r.keys()
    for key in keys:
        loan_ids.append(key.decode())

    # Generate transactions for the given day
    transactions = generate_transactions_for_day(loan_ids, day)

    # Create a Spark session
    spark = SparkSession.builder.appName("TransactionUpdater").getOrCreate()

    # Convert the transactions list to a Spark DataFrame
    df = spark.createDataFrame(transactions)

    # Write the DataFrame to a JSON file (overwrite the existing file)
    output_file = json_file_path + "_" + day

    # coalesce() operation reduces the number of partitions in the DataFrame. It combines the existing partitions into
    # a smaller number of partitions.
    # "overwrite": sets the write mode to "overwrite", which means that if the output file already exists,
    # it will be overwritten with the new data.
    df.coalesce(4).write.mode("overwrite").format("json").save(output_file)

    # Stop the Spark session
    spark.stop()


