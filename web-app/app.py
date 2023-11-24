"""place-holder"""

import os
import requests
import pymongo
from flask import Flask, request


app = Flask(__name__)

# Connecting to local host and same db as ml's backend
client = pymongo.MongoClient("mongodb://db:27017")
db = client["Isomorphism"]


# Views
@app.route("/")
@app.route("/<user_name>")
def display_songs(user_name=None):
    song_list = None
    if user_name:
        song_list = db.songs.find({"user_name": user_name})
    else:
        song_list = db.songs.find({})

    return render_template("home.html", song_list=song_list)


# Form handlers
@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    """upload audio"""
    audio_file = request.files["audio"]
    response = requests.post(
        "http://mlclient:5000/upload", files={"audio": audio_file}, timeout=5
    )
    return response.content, response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= os.getenv("PORT", 5000))
