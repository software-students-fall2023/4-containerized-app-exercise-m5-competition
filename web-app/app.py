"""web-page backend"""

from functools import wraps
import os
import uuid
import requests
import pymongo
import sounddevice as sd
import wavio
from flask import Flask, request, redirect, url_for, render_template, session, flash
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
# Connecting to local host and same db as ml's backend
client = pymongo.MongoClient("mongodb://db:27017")
db = client["Isomorphism"]

# Set secret key for sessions
app.secret_key = b"\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5"


# Utilities
def login_required(f):
    """login required decorators"""

    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        return redirect("/")

    return wrap


def start_session(user):
    """Create session containing user info"""
    del user["password"]
    session["logged_in"] = True
    session["user"] = user
    return redirect("/")


# Views
@app.route("/")
def homescreen_view():
    """upload audio"""
    return render_template("index.html")


@app.route("/transcripts")
@login_required
def transcripts_view():
    """View transcripts generated before by the user"""
    user_transcripts = db.history.find({"user_id": session["user"]["_id"]})
    return render_template("transcripts.html", transcripts=user_transcripts)


@app.route("/login")
def login_view():
    """Display log in page"""
    return render_template("logIn.html")


@app.route("/signup")
def signup_view():
    """Display sign up page"""
    return render_template("signUp.html")


@app.route("/transcription_result")
def transcription_result():
    """Display transcript result page"""
    return render_template("transcription_result.html")


# Form handlers


@app.route("/api/upload_audio", methods=["POST"])
def upload_audio():
    """call the ml client to do ML work"""
    audio_file = request.files["audio"]
    user_id = session["user"]["_id"] if "logged_in" in session else None
    data = {"user_id": user_id} if user_id else {}

    response = requests.post(
        "http://mlclient:5000/upload", files={"audio": audio_file}, data=data, timeout=5
    )

    if response.status_code == 200:
        result = response.json()
        return render_template("transcription_result.html", result=result)
    flash("Failed to process audio. Please try again.", "error")
    return redirect(url_for("homescreen_view"))


@app.route("/user/signup", methods=["POST"])
def signup():
    """sign up"""

    # Create the user object
    user = {
        "_id": uuid.uuid4().hex,
        "username": request.form.get("username"),
        "password": request.form.get("password"),
    }

    # Encrypt the password
    user["password"] = pbkdf2_sha256.encrypt(user["password"])

    if db.users.find_one({"username": user["username"]}):
        # Instead of rendering a template, use redirect with a message
        flash("Username already in use", "error")
        return redirect(url_for("signup_view"))

    if db.users.insert_one(user):
        return start_session(user)

    flash("Signup failed", "error")
    return redirect(url_for("signup_view"))


@app.route("/user/signout", methods=["POST"])
def signout():
    """signing out"""
    session.clear()
    return redirect("/")


@app.route("/user/login", methods=["POST"])
def login():
    """login"""
    user = db.users.find_one({"username": request.form.get("username")})
    if user and pbkdf2_sha256.verify(request.form.get("password"), user["password"]):
        return start_session(user)

    flash("Invalid Credentials", "error")
    return redirect(url_for("login_view"))


@app.route("/test_mic")
def test_mic():
    """test mic access"""
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording

    print("Recording...")
    rec = sd.rec(int(seconds * fs), samplerate=fs, channels=1, blocking=True)
    print(rec)
    sd.wait()  # Wait until recording is finished
    print("Recording finished")

    # Write the data to a WAV file
    wavio.write("output.wav", rec, fs, sampwidth=2)
    print("Saved as output.wav")
    return "success test of mic"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5001")))
