import sqlite3
from typing import List, Tuple, Optional

# Database connection
DB_PATH = "../../leads.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

# Insert Operations
def insert_linkedin_job(job_title: str, company: str, location: str, job_url: str, date_posted: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO linkedin_jobs (job_title, company, location, job_url, date_posted)
        VALUES (?, ?, ?, ?, ?)
    """, (job_title, company, location, job_url, date_posted))
    conn.commit()
    conn.close()


def insert_twitter_post(tweet_id: str, username: str, content: str, date: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO twitter_posts (tweet_id, username, content, date)
        VALUES (?, ?, ?, ?)
    """, (tweet_id, username, content, date))
    conn.commit()
    conn.close()


def insert_linkedin_post(post_id: str, username: str, content: str, date: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO linkedin_posts (post_id, username, content, date)
        VALUES (?, ?, ?, ?)
    """, (post_id, username, content, date))
    conn.commit()
    conn.close()


def insert_real_estate_transaction(title: str, company: str, location: str, transaction_type: str, date: str, source: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO real_estate_transactions (title, company, location, transaction_type, date, source)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, company, location, transaction_type, date, source))
    conn.commit()
    conn.close()


def insert_lead_tracking(source: str, reference_id: str, relevance_score: int, investigated: bool, notes: Optional[str] = None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO lead_tracking (source, reference_id, relevance_score, investigated, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (source, reference_id, relevance_score, investigated, notes))
    conn.commit()
    conn.close()


# Read Operations
def get_all_rows(table_name: str) -> List[Tuple]:
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_lead_by_id(lead_id: int) -> Optional[Tuple]:
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lead_tracking WHERE id = ?", (lead_id,))
    row = cursor.fetchone()
    conn.close()
    return row


# Update Operations
def update_lead_status(lead_id: int, investigated: bool, notes: Optional[str]):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE lead_tracking
        SET investigated = ?, notes = ?
        WHERE id = ?
    """, (investigated, notes, lead_id))
    conn.commit()
    conn.close()


def update_relevance_score(lead_id: int, new_score: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE lead_tracking
        SET relevance_score = ?
        WHERE id = ?
    """, (new_score, lead_id))
    conn.commit()
    conn.close()


# Delete Operations
def delete_row(table_name: str, row_id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (row_id,))
    conn.commit()
    conn.close()


# Utility Functions
def count_rows(table_name: str) -> int:
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def clear_table(table_name: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name}")
    conn.commit()
    conn.close()
