"""place-holder"""

import os
import requests
import pymongo
from flask import Flask, request


app = Flask(__name__)

# Connecting to local host and same db as ml's backend
client = pymongo.MongoClient("mongodb://db:27017")
db = client["Isomorphism"]


@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    """upload audio"""
    audio_file = request.files["audio"]
    response = requests.post(
        "http://mlclient:7001/upload", files={"audio": audio_file}, timeout=5
    )
    return response.content, response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "6001")))
