"""place-holder"""

import os
import json
import requests
import pymongo
from flask import Flask, request, render_template


app = Flask(__name__)

# Connecting to local host and same db as ml's backend
client = pymongo.MongoClient("mongodb://db:27017")
db = client["Isomorphism"]


# Views
@app.route("/")
def homescreen_view():
    """upload audio"""
    return render_template("index.html")


# Form handlers
@app.route("/api/upload_audio", methods=["POST"])
def upload_audio():
    """upload audio"""
    audio_file = request.files["audio"]
    try:
        response = requests.post(
            "http://mlclient:5000/upload", files={"audio": audio_file}, timeout=5
        )
    except requests.exceptions.Timeout:
        return {"error": "Timeout"}, 408
    # Decoding the byte string to a regular string
    response_text = response.content.decode("utf-8")

    # Parsing the JSON (optional, if you want to extract specific data)
    try:
        response_data = json.loads(response_text)
    except json.JSONDecodeError:
        # Handle error if response is not valid JSON
        response_data = {"error": "Invalid JSON response"}

    return render_template(
        "result.html", response_content=response_data, status_code=response.status_code
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
