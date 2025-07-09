#!/usr/bin/python3
"""
This module demonstrates how to run multiple database queries
concurrently using asyncio and the aiosqlite library.
"""
import asyncio
import aiosqlite
import time

DB_NAME = 'task_database.db'

async def async_fetch_users():
    """
    Asynchronously fetches all users from the database.
    """
    print("Task 1: Starting to fetch all users...")
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            result = await cursor.fetchall()
            # Simulate a slow network or I/O operation
            await asyncio.sleep(1)
            print("Task 1: Finished fetching all users.")
            return result

async def async_fetch_older_users():
    """
    Asynchronously fetches users older than 40.
    """
    print("Task 2: Starting to fetch older users...")
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            result = await cursor.fetchall()
            # Simulate another slow network or I/O operation
            await asyncio.sleep(1)
            print("Task 2: Finished fetching older users.")
            return result

async def fetch_concurrently():
    """
    Runs the two fetch functions concurrently using asyncio.gather.
    """
    print("--- Starting concurrent execution ---")
    start_time = time.time()
    
    # Create a list of the coroutine tasks to run
    tasks = [
        async_fetch_users(),
        async_fetch_older_users()
    ]
    
    # asyncio.gather runs all tasks concurrently and waits for them to complete
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"\n--- Concurrent execution finished in {end_time - start_time:.2f} seconds ---")
    
    # results will be a list containing the return values of the tasks
    all_users = results[0]
    older_users = results[1]
    
    print(f"\nFound {len(all_users)} total users.")
    print(f"Found {len(older_users)} users older than 40.")


# --- Main execution block ---
if __name__ == '__main__':
    # Ensure you have run setup_db.py first
    
    # asyncio.run() starts the asyncio event loop and runs the main coroutine
    asyncio.run(fetch_concurrently())