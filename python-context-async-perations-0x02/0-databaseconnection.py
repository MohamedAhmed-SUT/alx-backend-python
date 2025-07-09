#!/usr/bin/python3
"""
This module demonstrates a custom class-based context manager for
handling database connections automatically.
"""
import sqlite3

class DatabaseConnection:
    """
    A class-based context manager for SQLite database connections.
    """
    def __init__(self, db_name):
        """
        Initializes the context manager with the database file name.
        """
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """
        Called when entering the 'with' block.
        Establishes the database connection and returns it.
        """
        print(f"LOG: Opening connection to '{self.db_name}'...")
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting the 'with' block.
        Ensures the database connection is closed.
        
        The arguments exc_type, exc_val, exc_tb contain exception
        information if an error occurred inside the 'with' block.
        """
        if self.conn:
            print(f"LOG: Closing connection to '{self.db_name}'...")
            self.conn.close()
        
        # If an exception occurred, returning False will re-raise it.
        # Returning True would suppress it. We want it to be re-raised.
        return False

# --- Main execution block ---
if __name__ == '__main__':
    # Ensure you have run setup_db.py first to create 'task_database.db'
    db_file = 'task_database.db'
    
    print("--- Using the DatabaseConnection context manager ---")
    
    # The 'with' statement creates an instance of DatabaseConnection
    # and calls its __enter__ method. The returned connection object
    # is assigned to the variable 'conn'.
    try:
        with DatabaseConnection(db_file) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM users"
            print(f"Executing query: '{query}'")
            cursor.execute(query)
            results = cursor.fetchall()

            print("\nQuery Results:")
            for row in results:
                print(row)
    
        # Once the 'with' block is exited (either normally or via an error),
        # the __exit__ method is automatically called, closing the connection.
        print("\n--- Context manager has closed the connection. ---")

    except sqlite3.OperationalError as e:
        print(f"\nDatabase Error: {e}. Please run the setup_db.py script.")