import time
import tweepy
import sqlite3
import json
import os
import requests

# Load API credentials
config_path = os.path.join(os.path.dirname(__file__), "../../config.json")

with open(config_path, "r") as config_file:
    config = json.load(config_file)

BEARER_TOKEN = config["twitter_bearer_token"]

# Connect to Twitter API
client = tweepy.Client(bearer_token=BEARER_TOKEN)

QUERY = "changement de locaux lang:fr -is:retweet"
MAX_TWEETS = 1  # Reduce request load

url = "https://api.twitter.com/2/tweets/search/recent"
headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

response = requests.get("https://api.twitter.com/2/tweets/search/recent", headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.json())

def fetch_tweets():
    """Retrieve tweets and store them in the database, handling rate limits."""
    try:
        tweets = client.search_recent_tweets(
            query=QUERY, max_results=MAX_TWEETS, tweet_fields=["id", "text", "author_id", "created_at"]
        )

        if not tweets.data:
            print("Aucun tweet trouvé.")
            return

        db_conn = sqlite3.connect("../../leads.db")
        cursor = db_conn.cursor()

        for tweet in tweets.data:
            tweet_id = tweet.id
            username = f"user_{tweet.author_id}"  # Twitter API does not provide username in v2
            content = tweet.text
            date = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO twitter_posts (tweet_id, username, content, date) 
                VALUES (?, ?, ?, ?) 
                ON CONFLICT(tweet_id) DO NOTHING
            """, (tweet_id, username, content, date))

            cursor.execute("""
                INSERT INTO lead_tracking (source, reference_id, relevance_score, investigated, notes)
                VALUES (?, ?, ?, ?, ?)
            """, ("twitter", tweet_id, 50, 0, "Lead récupéré via Twitter"))

        db_conn.commit()
        db_conn.close()
        print(f"{len(tweets.data)} tweets enregistrés en base de données.")

    except tweepy.errors.TooManyRequests:
        print("Rate limit exceeded. Waiting for reset.")
if __name__ == "__main__":
    fetch_tweets()
