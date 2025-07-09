#!/usr/bin/python3
"""
This file contains the solution for Task 0.
"""
import sqlite3
import functools

# --- This is the part you need to write (the Decorator) ---
def log_queries(func):
    """
    This is the decorator. Its job is to take a function as input,
    add the functionality of logging (printing) the SQL query, 
    then return the new function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # *args: positional arguments (e.g., "SELECT * FROM users")
        # **kwargs: keyword arguments (e.g., query="SELECT * FROM users")
        
        # Step 1: Search for the SQL query in the inputs
        query = None
        if args:
            query = args[0]  # Assume the query is the first argument
        elif 'query' in kwargs:
            query = kwargs['query']  # If passed as a keyword argument
        
        # Step 2: Print (log) the query if found
        if query:
            print(f"LOG: Executing query: '{query}'")
        
        # Step 3: Call the original decorated function
        # and return its result
        return func(*args, **kwargs)
    
    # The decorator must return the inner function (wrapper)
    return wrapper

# --- This code is given for testing in the task ---

# Here we use the decorator to decorate the function
@log_queries
def fetch_all_users(query):
    """This function fetches users from the database."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# --- This line runs the function to test the decorator ---
# This part is called the "main execution block"
if __name__ == '__main__':
    print("Starting user fetch operation...")
    users = fetch_all_users("SELECT * FROM users")
    print("\nQuery executed. Results:")
    print(users)
