import sqlite3

db_conn = sqlite3.connect("leads.db")
cursor = db_conn.cursor()

linkedin_job = ("Facility Manager", "Test Company", "Paris, France", "https://linkedin.com/job/test", "2025-02-17")
twitter_post = ("1234567890", "test_user", "We're moving to a new office in Paris! #relocation", "2025-02-17")
linkedin_post = ("9876543210", "company_page", "Excited about our new headquarters!", "2025-02-17")
real_estate_transaction = ("Office Lease", "Big Corp", "Lyon, France", "Lease", "2025-02-16", "Le Figaro Immobilier")
lead_tracking = ("twitter", "1234567890", 80, 0, "Potential lead")

cursor.execute("INSERT INTO linkedin_jobs (job_title, company, location, job_url, date_posted) VALUES (?, ?, ?, ?, ?)", linkedin_job)
cursor.execute("INSERT INTO twitter_posts (tweet_id, username, content, date) VALUES (?, ?, ?, ?)", twitter_post)
cursor.execute("INSERT INTO linkedin_posts (post_id, username, content, date) VALUES (?, ?, ?, ?)", linkedin_post)
cursor.execute("INSERT INTO real_estate_transactions (title, company, location, transaction_type, date, source) VALUES (?, ?, ?, ?, ?, ?)", real_estate_transaction)
cursor.execute("INSERT INTO lead_tracking (source, reference_id, relevance_score, investigated, notes) VALUES (?, ?, ?, ?, ?)", lead_tracking)

db_conn.commit()
db_conn.close()

print("Test data inserted successfully!")
