#!/usr/bin/python3
"""
This module demonstrates a decorator for automatically managing
database connections, reducing boilerplate code.
"""
import sqlite3
import functools

def with_db_connection(func):
    """
    A decorator that handles the database connection lifecycle.
    It opens a connection, passes it as the first argument ('conn') to the
    decorated function, and ensures the connection is closed afterwards.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # The 'conn' object will be managed entirely within this wrapper.
        conn = None
        try:
            # 1. Open the database connection
            conn = sqlite3.connect('users.db')
            
            # 2. Call the original function, passing the connection
            #    object as the first positional argument.
            result = func(conn, *args, **kwargs)
            
            # 4. Return the result from the original function
            return result
        except Exception as e:
            # If any error occurs, print it and re-raise it.
            print(f"An error occurred: {e}")
            raise
        finally:
            # 5. Ensure the connection is closed, no matter what.
            if conn:
                conn.close()
                # print("LOG: Database connection closed.") # Optional log
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a single user by their ID using the provided connection.
    The @with_db_connection decorator automatically provides and closes the 'conn' object.
    Notice how clean this function is - no connection logic inside!
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# --- Fetch user by ID with automatic connection handling ---
if __name__ == '__main__':
    # Make sure you have run setup_db.py first
    print("Fetching user with ID 1...")
    user = get_user_by_id(user_id=1)
    print(user)

    print("\nFetching user with ID 99 (should not exist)...")
    user_not_found = get_user_by_id(user_id=99)
    print(user_not_found)