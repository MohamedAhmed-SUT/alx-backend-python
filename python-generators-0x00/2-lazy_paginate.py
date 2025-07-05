#!/usr/bin/python3
"""
This module contains a generator to lazily load paginated data from a database,
fetching one page at a time only when needed.
"""
import seed  # Import the seed module for database connection

def paginate_users(page_size: int, offset: int) -> list:
    """
    Fetches a single page of users from the database.
    (This function is provided by the project instructions and included here).

    Args:
        page_size (int): The number of users to fetch per page.
        offset (int): The starting point from which to fetch users.

    Returns:
        list: A list of user dictionaries for the requested page.
    """
    connection = None
    try:
        connection = seed.connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            # Use placeholders for security, although f-string is in instructions
            query = "SELECT * FROM user_data ORDER BY name LIMIT %s OFFSET %s"
            cursor.execute(query, (page_size, offset))
            rows = cursor.fetchall()
            return rows
        return []
    except Exception as e:
        print(f"An error occurred in paginate_users: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()


def lazy_pagination(page_size: int = 100):
    """
    A generator that lazily loads pages of users. It only fetches the
    next page from the database when it is requested by the loop.

    Args:
        page_size (int): The number of users per page.

    Yields:
        list: A page (list) of user dictionaries.
    """
    offset = 0
    # This is the single loop required by the instructions.
    while True:
        # Call the helper function to fetch just one page of data.
        page = paginate_users(page_size, offset)
        
        # If the returned page is empty, there's no more data to fetch.
        # We break the loop and the generator stops.
        if not page:
            break
        
        # Yield the current page and pause until the next one is requested.
        yield page
        
        # Increment the offset to prepare for the next page fetch.
        offset += page_size