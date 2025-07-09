#!/usr/bin/python3
"""
This module demonstrates a more advanced context manager that not only
handles the database connection but also executes a query.
"""
import sqlite3

class ExecuteQuery:
    """
    A reusable context manager that connects to a database, executes
    a given query with parameters, and provides the cursor to fetch results.
    """
    def __init__(self, db_name, query, params=()):
        """
        Initializes the context manager.

        Args:
            db_name (str): The name of the database file.
            query (str): The SQL query string to be executed.
            params (tuple, optional): A tuple of parameters for the query.
                                      Defaults to an empty tuple.
        """
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None

    def __enter__(self):
        """
        Called when entering the 'with' block.
        Connects to the DB, creates a cursor, executes the query,
        and returns the cursor.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            cursor = self.conn.cursor()
            print(f"LOG: Executing query: '{self.query}' with params {self.params}")
            cursor.execute(self.query, self.params)
            return cursor
        except Exception as e:
            # If an error happens during setup, close connection and re-raise
            if self.conn:
                self.conn.close()
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting the 'with' block.
        Ensures the database connection is closed.
        """
        if self.conn:
            self.conn.close()
        
        # We don't suppress exceptions
        return False

# --- Main execution block ---
if __name__ == '__main__':
    # Ensure you have run setup_db.py first
    db_file = 'task_database.db'
    
    # Define the query and parameters as per the instructions
    sql_query = "SELECT * FROM users WHERE age > ?"
    age_param = (25,) # Parameters must be in a tuple

    print("--- Using the ExecuteQuery context manager ---")
    
    try:
        # The 'with' statement creates an instance and calls __enter__.
        # The returned cursor is assigned to the variable 'results_cursor'.
        with ExecuteQuery(db_file, sql_query, age_param) as results_cursor:
            # Now we just need to fetch the results from the cursor
            results = results_cursor.fetchall()

            print("\nQuery Results (users older than 25):")
            if results:
                for row in results:
                    print(row)
            else:
                print("No users found matching the criteria.")
        
        # __exit__ is automatically called here, closing the connection.
        print("\n--- Context manager has finished and closed the connection. ---")

    except sqlite3.OperationalError as e:
        print(f"\nDatabase Error: {e}. Please run the setup_db.py script.")