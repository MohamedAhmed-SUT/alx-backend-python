#!/usr/bin/python3
"""
This script provides functions to set up and seed a MySQL database
for the ALX ProDev Python Generators project.
"""
import mysql.connector
import os
import csv

def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database in MYSQL."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields."""
    cursor = connection.cursor()
    # Note: MySQL doesn't have a native UUID type like PostgreSQL. VARCHAR(36) is standard.
    # DECIMAL for age is unusual; INT is more standard. We will use INT here.
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age INT NOT NULL,
        INDEX(user_id)
    )
    """
    try:
        cursor.execute(create_table_query)
        print("Table user_data created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data):
    """Inserts data from a CSV file into the database if the table is empty."""
    cursor = connection.cursor()
    try:
        # Check if table is empty before inserting to prevent duplicates
        cursor.execute("SELECT COUNT(*) FROM user_data")
        if cursor.fetchone()[0] > 0:
            print("Data already exists in user_data. Skipping insertion.")
            return

        with open(data, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip the header row
            sql = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
            
            # The csv reader gives strings, so we convert age to int
            data_to_insert = [(row[0], row[1], row[2], int(row[3])) for row in reader]
            
            cursor.executemany(sql, data_to_insert)
            connection.commit()
            print(f"{cursor.rowcount} records inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        connection.rollback()
    except FileNotFoundError:
        print(f"Error: The file {data} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        cursor.close()