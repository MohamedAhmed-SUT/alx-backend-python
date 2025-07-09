#!/usr/bin/python3
"""
This module demonstrates decorators for connection and transaction
management, ensuring data integrity during database operations.
"""
import sqlite3
import functools

# --- Decorator from previous task (required) ---
def with_db_connection(func):
    """
    Decorator to handle the database connection lifecycle.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            result = func(conn, *args, **kwargs)
            return result
        except Exception as e:
            print(f"An error occurred in the connection wrapper: {e}")
            raise
        finally:
            if conn:
                conn.close()
    return wrapper

# --- New decorator for this task ---
def transactional(func):
    """
    A decorator that wraps a function in a database transaction.
    It commits the transaction if the function executes successfully,
    and rolls back if any exception occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # In sqlite3, a transaction is implicitly started with the first
            # data-modifying statement (like INSERT, UPDATE, DELETE).
            print(f"LOG: Starting transaction for function '{func.__name__}'...")
            
            result = func(conn, *args, **kwargs)
            
            # If the function completes without errors, commit the changes.
            conn.commit()
            print("LOG: Transaction committed successfully.")
            return result
        except Exception as e:
            # If any error occurs, roll back all changes made during the transaction.
            print(f"LOG: An error occurred. Rolling back transaction: {e}")
            if conn:
                conn.rollback()
            # Re-raise the exception so it can be handled by other parts of the code.
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Updates a user's email within a transaction."""
    print(f"Executing: UPDATE users SET email = '{new_email}' WHERE id = {user_id}")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    # To test the rollback, you could add a line here that causes an error,
    # for example: raise ValueError("Simulating a failure during transaction")

# --- Update user's email with automatic transaction handling ---
if __name__ == '__main__':
    # Make sure you have run setup_db.py first
    
    # --- Verify initial state ---
    conn_check = sqlite3.connect('users.db')
    cursor_check = conn_check.cursor()
    cursor_check.execute("SELECT email FROM users WHERE id=1")
    initial_email = cursor_check.fetchone()[0]
    print(f"Initial email for user 1: {initial_email}")
    conn_check.close()
    
    # --- Perform a successful update ---
    try:
        new_email = 'alice.smith@example.com'
        update_user_email(user_id=1, new_email=new_email)
    except Exception:
        pass # Ignore exceptions for this demonstration
    
    # --- Verify final state ---
    conn_check = sqlite3.connect('users.db')
    cursor_check = conn_check.cursor()
    cursor_check.execute("SELECT email FROM users WHERE id=1")
    final_email = cursor_check.fetchone()[0]
    print(f"Final email for user 1: {final_email}")
    conn_check.close()
    
    # --- Reset for next run ---
    conn_reset = sqlite3.connect('users.db')
    conn_reset.execute("UPDATE users SET email = ? WHERE id = ?", (initial_email, 1))
    conn_reset.commit()
    conn_reset.close()
    print("\nEmail has been reset for the next run.")