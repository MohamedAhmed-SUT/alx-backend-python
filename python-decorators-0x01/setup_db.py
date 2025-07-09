import sqlite3

def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    users_to_add = [(1, 'Alice', 'a@a.com'), (2, 'Bob', 'b@b.com')]
    try:
        cursor.executemany('INSERT INTO users (id, name, email) VALUES (?, ?, ?)', users_to_add)
    except sqlite3.IntegrityError:
        pass # Data already exists
    conn.commit()
    conn.close()
    print("Database 'users.db' is ready.")

if __name__ == '__main__':
    setup_database()