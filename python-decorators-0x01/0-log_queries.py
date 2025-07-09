#!/usr/bin/python3
"""
This module demonstrates a simple Python decorator to log SQL queries
with a timestamp, as required by the checker.
"""
import sqlite3
import functools
from datetime import datetime  # <--- هذا هو السطر المطلوب إضافته

# --- decorator to log SQL queries ---
def log_queries(func):
    """
    A decorator that logs the SQL query string along with a timestamp
    before executing the function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # --- هذا هو الجزء الذي تم تعديله ---
        
        # الحصول على الوقت والتاريخ الحالي
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # البحث عن استعلام SQL في المدخلات
        query = None
        if args:
            query = args[0]
        elif 'query' in kwargs:
            query = kwargs['query']
        
        # طباعة رسالة التسجيل مع الوقت والتاريخ
        if query:
            print(f"[{timestamp}] LOG: Executing query: '{query}'")
        else:
            print(f"[{timestamp}] LOG: No query string found in arguments to log.")
        
        # ------------------------------------
        
        # تشغيل الدالة الأصلية
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """Fetches all users from the database based on a query."""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}. Please run the setup_db.py script first.")
        return []
    finally:
        if 'conn' in locals() and conn:
            conn.close()

# --- fetch users while logging the query ---
if __name__ == '__main__':
    # لا داعي لتغيير هذا الجزء
    print("Attempting to fetch users...")
    users = fetch_all_users("SELECT * FROM users")
    print("\nQuery has been executed. Results:")
    print(users)