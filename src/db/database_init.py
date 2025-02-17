import sqlite3

def initialize_database():
    db_conn = sqlite3.connect("leads.db")
    cursor = db_conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS linkedin_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT,
            company TEXT,
            location TEXT,
            job_url TEXT,
            date_posted TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS twitter_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet_id TEXT UNIQUE,
            username TEXT,
            content TEXT,
            date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS linkedin_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id TEXT UNIQUE,
            username TEXT,
            content TEXT,
            date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS real_estate_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            transaction_type TEXT,
            date TEXT,
            source TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lead_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            reference_id TEXT UNIQUE,
            relevance_score INTEGER,
            investigated BOOLEAN DEFAULT 0,
            notes TEXT
        )
    ''')
    
    db_conn.commit()
    db_conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
