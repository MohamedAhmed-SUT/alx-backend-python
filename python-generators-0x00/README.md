# alx-backend-python

# Python Generators Project

This project explores the use of Python generators for memory-efficient data processing, especially when working with large datasets from a database.

## Task 0: Database Seeding Script

The `seed.py` script is the foundation for this project. It contains a set of functions responsible for:
1.  **Connecting** to a MySQL server using credentials from environment variables.
2.  **Creating** the `ALX_prodev` database if it doesn't already exist.
3.  **Creating** the `user_data` table with the specified schema (`user_id`, `name`, `email`, `age`).
4.  **Seeding** the table with sample data from the `user_data.csv` file, ensuring data is not inserted more than once.

This script is imported by all subsequent task files to establish a database connection and interact with the data.


---

## Task 1: Stream Users with a Generator

The `0-stream_users.py` script contains the `stream_users()` function.

This function is a **generator** that connects to the database and fetches users one by one using the `yield` keyword. This approach is highly memory-efficient, as it avoids loading the entire `user_data` table into memory at once. It returns each user as a dictionary for convenient use.


---

## Task 2: Batch Processing Large Data

The `1-batch_processing.py` script demonstrates a more performant way to process data by handling it in batches.

- **`stream_users_in_batches(batch_size)`**: This generator uses the cursor's `fetchmany()` method to yield lists of users (batches) instead of individual users. This reduces the number of interactions with the database, improving efficiency.
- **`batch_processing(batch_size)`**: This function consumes the batches from the generator and then processes each user within the batch, in this case, filtering for users older than 25.