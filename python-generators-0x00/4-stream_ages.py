#!/usr/bin/python3
"""
This module demonstrates memory-efficient aggregation by using a generator
to calculate the average age of all users in a database without
loading the entire dataset into memory.
"""
import seed  # Import the seed module for database connection

def stream_user_ages():
    """
    A generator that connects to the database and yields the age
    of each user, one by one.
    """
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            return

        cursor = connection.cursor()
        # We only need the 'age' column, which is more efficient
        cursor.execute("SELECT age FROM user_data")

        # This is the first loop, iterating through the cursor
        for row in cursor:
            yield row[0]  # Yield only the age value (the first column)

    except Exception as e:
        print(f"An error occurred while streaming ages: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def calculate_average_age():
    """
    Consumes the stream_user_ages generator to calculate the average
    age in a memory-efficient manner.
    """
    total_age = 0
    user_count = 0

    # This is the second loop, consuming the generator
    for age in stream_user_ages():
        total_age += age
        user_count += 1
    
    if user_count == 0:
        average_age = 0
    else:
        average_age = total_age / user_count

    print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    # This block makes the script runnable from the command line
    calculate_average_age()