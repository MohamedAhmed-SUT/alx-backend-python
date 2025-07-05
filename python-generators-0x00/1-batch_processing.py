#!/usr/bin/python3
"""
This module contains functions to stream and process user data in batches
for improved performance when handling large datasets.
"""
import seed  # Import the seed module for database connection

def stream_users_in_batches(batch_size=50):
    """
    A generator function that connects to the database and yields
    batches of user rows.

    Args:
        batch_size (int): The number of rows to fetch in each batch.

    Yields:
        list: A list of dictionaries, where each dictionary represents a user.
    """
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            return

        # Use a dictionary cursor to get rows as dictionaries
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data ORDER BY name;")

        # This is the first loop (the main fetching loop)
        while True:
            # fetchmany() is an efficient way to get a specific number of rows
            batch = cursor.fetchmany(batch_size)
            
            # If fetchmany returns an empty list, we've reached the end
            if not batch:
                break
            
            # Yield the entire batch (a list of user dictionaries)
            yield batch

    except Exception as e:
        print(f"An error occurred while streaming batches: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size=50):
    """
    Processes batches of users to filter and print users older than 25.

    Args:
        batch_size (int): The size of the batches to process.
    """
    # This is the second loop (iterating over the batches yielded by the generator)
    for user_batch in stream_users_in_batches(batch_size):
        # This is the third loop (iterating over users within a single batch)
        for user in user_batch:
            if user.get('age', 0) > 25:
                print(user)