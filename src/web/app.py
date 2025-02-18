from flask import Flask, render_template, request, redirect, url_for, flash
from src.db.database import get_all_rows, get_lead_by_id, update_lead_status, delete_row, count_rows

# Initialize Flask App
app = Flask(__name__)
app.secret_key = "supersecretkey"  # For flashing messages

# Homepage: Display Leads
table_names = ["linkedin_jobs", "twitter_posts", "linkedin_posts", "real_estate_transactions"]
@app.route('/')
def index():
    leads = get_all_rows("lead_tracking")
    return render_template("index.html", leads=leads, total_leads=count_rows("lead_tracking"))

# Lead Details Page
@app.route('/lead/<int:lead_id>', methods=['GET', 'POST'])
def lead_details(lead_id):
    lead = get_lead_by_id(lead_id)
    if not lead:
        flash("Lead not found!", "danger")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        investigated = request.form.get("investigated") == "on"
        notes = request.form.get("notes")
        update_lead_status(lead_id, investigated, notes)
        flash("Lead updated successfully!", "success")
        return redirect(url_for('index'))
    
    return render_template("lead_details.html", lead=lead)

# Delete Lead
@app.route('/delete/<int:lead_id>', methods=['POST'])
def delete_lead(lead_id):
    delete_row("lead_tracking", lead_id)
    flash("Lead deleted successfully!", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
