"""place-holder"""

import os
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
    response = requests.post(
        "http://mlclient:5000/upload", files={"audio": audio_file}, timeout=5
    )
    return response.content, response.status_code

@app.route("/api/upload_photo", methods=["POST"])
def upload_photo():
    """upload photo"""
    photo_file = request.files["photo"]

    response = requests.post(
        "http://mlclient:5000/upload_photo", files={"photo": photo_file}, timeout=20
    )
    return response.content, response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
