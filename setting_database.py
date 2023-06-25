from SQL_manager import DatabaseConnector


def setup_database():
    """
    This function creates three tables in the CREDIT_RECORDS.db
    """
    db = DatabaseConnector('CREDIT_RECORDS.db')

    loan_records = '''CREATE TABLE IF NOT EXISTS loan_records
                        (Loan_ID TEXT,
                        Customer_ID TEXT,
                        Name_Surname TEXT,
                        Age INTEGER,
                        Education TEXT,
                        Income INTEGER,
                        CRIF_delay INTEGER,
                        CR_suffering TEXT,
                        CoApplicant TEXT,
                        Dependents_No INTEGER,
                        Savings INTEGER,
                        CoApp_Income INTEGER,
                        Amount INTEGER,
                        Purpose TEXT,
                        Term TEXT,
                        Status TEXT)'''

    db.execute_query(loan_records)

    fully_paid = '''CREATE TABLE IF NOT EXISTS fully_paid
                            (Loan_ID TEXT,
                            Amount INTEGER,
                            Monthly_dept INTEGER,
                            Interest_rate INTEGER,
                            Duration INTEGER,
                            Delay INTEGER,
                            Last_Fee INTEGER)'''

    db.execute_query(fully_paid)

    ongoing_records = '''CREATE TABLE IF NOT EXISTS ongoing
                            AS SELECT * FROM loan_records WHERE 0'''

    db.execute_query(ongoing_records)
    db.close()