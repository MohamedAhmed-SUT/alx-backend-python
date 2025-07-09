#!/usr/bin/python3
"""
This module demonstrates a decorator that can retry a function
if it fails, making the application more resilient to transient errors.
"""
import time
import sqlite3
import functools

# --- Decorator from a previous task (required) ---
def with_db_connection(func):
    """Decorator to handle the database connection lifecycle."""
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
def retry_on_failure(retries=3, delay=1):
    """
    A decorator factory that makes a function retry its execution
    upon failure.

    Args:
        retries (int): The maximum number of attempts.
        delay (int): The number of seconds to wait between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    # Attempt to execute the decorated function
                    return func(*args, **kwargs)
                except Exception as e:
                    # If it fails, log the attempt and error
                    print(f"LOG: Attempt {i + 1} of {retries} failed: {e}")
                    
                    # If this was the last attempt, re-raise the exception
                    if i == retries - 1:
                        print("LOG: All retries failed. Raising exception.")
                        raise
                    
                    # Wait for the specified delay before the next attempt
                    print(f"LOG: Retrying in {delay} second(s)...")
                    time.sleep(delay)
        return wrapper
    return decorator

# A variable to simulate failures for testing purposes
# We will make the first two attempts fail
ATTEMPT_COUNTER = 0

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetches users. This function is designed to fail a few times
    to demonstrate the retry decorator.
    """
    global ATTEMPT_COUNTER
    ATTEMPT_COUNTER += 1
    
    print(f"\n--- Inside fetch_users_with_retry (Attempt #{ATTEMPT_COUNTER}) ---")
    
    # Simulate a transient error for the first 2 attempts
    if ATTEMPT_COUNTER < 3:
        print("Simulating a database connection error...")
        raise sqlite3.OperationalError("Mock Error: database is temporarily unavailable")
    
    # On the 3rd attempt, it will succeed
    print("Connection successful!")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# --- attempt to fetch users with automatic retry on failure ---
if __name__ == '__main__':
    # Make sure you have run setup_db.py first
    print("--- Starting fetch process ---")
    try:
        users = fetch_users_with_retry()
        print("\n--- Final Result ---")
        print("Successfully fetched users:")
        print(users)
    except Exception as e:
        print(f"\n--- Final Result ---")
        print(f"The operation failed after all retries: {e}")