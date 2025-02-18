import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from src.db.database import get_all_rows, get_lead_by_id, update_lead_status, delete_row, count_rows
from src.api.twitter import fetch_tweets

# Initialize Flask App
app = Flask(__name__)
app.secret_key = "supersecretkey"  # For flashing messages

# Homepage: Display Leads
table_names = ["linkedin_jobs", "twitter_posts", "linkedin_posts", "real_estate_transactions"]

@app.route('/')
def index():
    filter_option = request.args.get("filter", "all")  # Default: "all"
    source_option = request.args.get("source", "all")  # Default: "all"
    sort_option = request.args.get("sort", "none")  # Default: "none"

    db_conn = sqlite3.connect("../../leads.db")
    cursor = db_conn.cursor()

    # Build dynamic SQL query
    query = "SELECT * FROM lead_tracking WHERE 1=1"
    params = []

    if filter_option == "investigated":
        query += " AND investigated = 1"
    elif filter_option == "not_investigated":
        query += " AND investigated = 0"

    if source_option in ["twitter", "linkedin", "real_estate"]:
        query += " AND source = ?"
        params.append(source_option)

    # Add sorting condition
    if sort_option == "asc":
        query += " ORDER BY relevance_score ASC"
    elif sort_option == "desc":
        query += " ORDER BY relevance_score DESC"

    cursor.execute(query, params)
    leads = cursor.fetchall()
    db_conn.close()

    return render_template("index.html", leads=leads, filter=filter_option, source=source_option, sort=sort_option)

@app.route('/run_twitter_scraper', methods=['POST'])
def run_twitter_scraper():
    try:
        fetch_tweets()  # Exécuter directement la fonction du scraper
        flash("Collecte Twitter terminée avec succès.", "success")
    except Exception as e:
        flash(f"Erreur lors de la collecte : {str(e)}", "danger")

    return redirect(url_for('index'))

# Lead Details Page
@app.route('/lead/<int:lead_id>', methods=['GET', 'POST'])
def lead_details(lead_id):
    lead = get_lead_by_id(lead_id)  # Fetch lead from database
    
    if not lead:
        flash("Lead not found!", "danger")
        return redirect(url_for('index'))

    # Fetch additional details based on lead source
    extra_info = None
    source = lead[1]  # 'twitter', 'linkedin', or 'real_estate'

    db_conn = sqlite3.connect("../../leads.db")
    cursor = db_conn.cursor()

    if source == "twitter":
        cursor.execute("SELECT tweet_id, username, content FROM twitter_posts WHERE id = ?", (lead[0],))
        extra_info = cursor.fetchone()
    elif source == "linkedin":
        cursor.execute("SELECT job_title, company FROM linkedin_jobs WHERE id = ?", (lead[0],))
        extra_info = cursor.fetchone()
    elif source == "real_estate":
        cursor.execute("SELECT transaction_type, location FROM real_estate_transactions WHERE id = ?", (lead[0],))
        extra_info = cursor.fetchone()

    db_conn.close()

    if request.method == 'POST':
        investigated = request.form.get("investigated") == "on"
        notes = request.form.get("notes")
        update_lead_status(lead_id, investigated, notes)
        flash("Lead updated successfully!", "success")
        return redirect(url_for('index'))

    return render_template("lead_details.html", lead=lead, extra_info=extra_info)

# Delete Lead
@app.route('/delete/<int:lead_id>', methods=['POST'])
def delete_lead(lead_id):
    delete_row("lead_tracking", lead_id)
    flash("Lead deleted successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
