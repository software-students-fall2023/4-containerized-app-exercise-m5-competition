"""place-holder"""
from functools import wraps
import os
import requests
import pymongo
from flask import Flask, request, render_template, redirect, session

app = Flask(__name__)
# Connecting to local host and same db as ml's backend
client = pymongo.MongoClient("mongodb://db:27017")
db = client["Isomorphism"]

# Login require decorators
def login_required(f):
    """login required decorators"""
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap

# Views
@app.route("/")
def homescreen_view():
    """upload audio"""
    return render_template("index.html")


@app.route("/transcripts")
@login_required
def transcripts_view():
    """View transcripts generated before by the user"""
    return render_template("transcripts.html")



# Form handlers
@app.route("/api/upload_audio", methods=["POST"])
def upload_audio():
    """upload audio"""
    audio_file = request.files["audio"]
    response = requests.post(
        "http://mlclient:5000/upload", files={"audio": audio_file}, timeout=5
    )
    return response.content, response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
