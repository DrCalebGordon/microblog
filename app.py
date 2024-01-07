from pymongo import MongoClient
from flask import Flask, render_template, request
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = pymongo.MongoClient("mongodb+srv://drcalebgordon:Heath.2017@microblog.dnytkbt.mongodb.net/", tlsCAFile=certifi.where())
    app.db = client.microblog

    # Get the current date and time
    current_datetime = datetime.now()
    current_date = current_datetime.date()

    @app.route('/', methods=["GET", "POST"])
    def home_page():
        entries_with_date = []

        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        # Fetch entries outside of the POST block to handle both GET and POST requests
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d, %Y")
            )
            for entry in app.db.entries.find({})
        ]

        return render_template("index.html", entries=entries_with_date, current_date=current_date)

    if __name__ == '__main__':
        app.run()

    return app
