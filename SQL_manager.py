import sqlite3

class DatabaseConnector:
    """
    This class defines all the functions we need to work inside the database
    """
    def __init__(self, database_name):
        """
        Database connecting function
        """
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, parameters=None):
        """
        Executing query function
        """
        if parameters:
            self.cursor.execute(query, parameters)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def execute_query_by_loan_id(self, loan_id, table_name, column):
        self.execute_query(f"SELECT {column} FROM {table_name} WHERE loan_id = ?", (loan_id,))
        element = self.fetchone()
        return element[0]

    def fetchall(self):
        """
        Retrieves all the results of a query executed via the cursor
        """
        return self.cursor.fetchall()

    def fetchone(self):
        """
        Retrieves one result of the query executed via the cursor
        """
        return self.cursor.fetchone()

    def get_column_names(self, table_name):
        """
        Returning column names
        """
        query = f"PRAGMA table_info({table_name})"
        self.cursor.execute(query)
        columns = [column[1] for column in self.cursor.fetchall()]
        return columns

    def close(self):
        """
        Database connection closing function
        """
        self.cursor.close()
        self.connection.close()

