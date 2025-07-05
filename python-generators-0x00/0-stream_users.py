#!/usr/bin/python3
"""
This module contains a generator function that streams user data
row by row from a MySQL database.
"""
import seed  # Import the seed module to use its connection functions

def stream_users():
    """
    A generator function that connects to the ALX_prodev database
    and yields user rows one by one.

    Each row is returned as a dictionary for easy access to column data.
    """
    connection = None
    cursor = None
    try:
        # Establish a connection to the database
        connection = seed.connect_to_prodev()
        if not connection:
            # If connection fails, the generator stops
            return

        # Using dictionary=True makes the cursor return rows as dictionaries
        # (e.g., {'user_id': '...', 'name': '...'}), which matches the expected output.
        cursor = connection.cursor(dictionary=True)

        # Execute the query to fetch all users
        cursor.execute("SELECT * FROM user_data ORDER BY name;")

        # This is the single loop required by the instructions.
        # The cursor itself is an iterator, so we can loop over it.
        # It fetches rows from the database as needed, not all at once.
        for row in cursor:
            yield row

    except Exception as e:
        print(f"An error occurred while streaming users: {e}")
    finally:
        # Ensure the cursor and connection are closed properly
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


