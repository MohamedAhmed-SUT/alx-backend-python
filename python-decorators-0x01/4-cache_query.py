#!/usr/bin/python3
"""
This module demonstrates a decorator for caching database query results
to improve performance by avoiding redundant database calls.
"""
import time
import sqlite3
import functools

# A simple in-memory cache implemented as a dictionary
query_cache = {}

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
def cache_query(func):
    """
    A decorator that caches the results of a function based on its arguments.
    It uses the SQL query string as the key for the cache.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a unique key for the cache. A simple way is to use the
        # string representation of all arguments. For this task, we focus
        # on the 'query' argument.
        
        # Find the query string from either positional or keyword arguments
        query = kwargs.get('query')
        if not query and args:
            # Assumes the query is the second argument after 'conn'
            if len(args) > 1:
                query = args[1]

        # Use the query string as the cache key
        cache_key = query

        # Check if the result is already in the cache
        if cache_key in query_cache:
            print(f"LOG: Returning result from cache for key: '{cache_key}'")
            return query_cache[cache_key]

        # If not in cache, execute the function
        print(f"LOG: Query not in cache. Executing and caching result for key: '{cache_key}'")
        result = func(*args, **kwargs)
        
        # Store the result in the cache
        query_cache[cache_key] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetches users from the database. This function is decorated
    to cache its results.
    """
    print("--- Executing database query (this should only happen once) ---")
    # Simulate a slow query to make the effect of caching more obvious
    time.sleep(2)
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# --- Main execution block to demonstrate caching ---
if __name__ == '__main__':
    # Make sure you have run setup_db.py first
    
    query_string = "SELECT * FROM users ORDER BY name"

    print("--- First Call (should be slow and will populate the cache) ---")
    start_time_1 = time.time()
    users_1 = fetch_users_with_cache(query=query_string)
    end_time_1 = time.time()
    print(f"Result 1: {users_1}")
    print(f"Time taken for first call: {end_time_1 - start_time_1:.2f} seconds\n")

    print("--- Second Call (should be very fast and use the cache) ---")
    start_time_2 = time.time()
    users_2 = fetch_users_with_cache(query=query_string)
    end_time_2 = time.time()
    print(f"Result 2: {users_2}")
    print(f"Time taken for second call: {end_time_2 - start_time_2:.2f} seconds\n")
    
    # Verify that the results are the same
    assert users_1 == users_2
    print("Assertion passed: Results from both calls are identical.")
    print(f"\nCurrent cache state: {query_cache}")