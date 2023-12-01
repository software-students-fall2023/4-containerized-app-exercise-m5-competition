"""web-page backend"""

from functools import wraps
import os
import uuid
import json
import requests
import pymongo
import mongomock
from flask import (
    Flask,
    request,
    redirect,
    url_for,
    render_template,
    session,
    flash,
    jsonify,
)
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

# Use mongomock for testing, else use the real MongoClient
if os.environ.get("TESTING"):
    client = mongomock.MongoClient()
else:
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
    """Display transcript result page with the transcription results"""
    result_json = request.args.get("result", "{}")
    result = json.loads(result_json)
    return render_template("transcription_result.html", result=result)


# Form handlers


@app.route("/api/js_upload_audio", methods=["POST"])
def js_upload_audio():
    """Endpoint specifically for JavaScript to upload audio and get JSON response"""
    audio_file = request.files["audio"]
    if not audio_file:
        return jsonify({"error": "No audio file provided"}), 400

    user_id = session["user"]["_id"] if "logged_in" in session else None
    data = {"user_id": user_id} if user_id else {}

    response = requests.post(
        "http://mlclient:5000/upload",
        files={"audio": audio_file},
        data=data,
        timeout=10,
    )

    if response.status_code == 200:
        return jsonify(response.json()), 200
    return (
        jsonify({"error": "Error processing audio", "details": response.text}),
        response.status_code,
    )


@app.route("/api/upload_audio", methods=["POST"])
def upload_audio():
    """call the ml client to do ML work"""
    audio_file = request.files["audio"]
    user_id = session["user"]["_id"] if "logged_in" in session else None
    data = {"user_id": user_id} if user_id else {}

    response = requests.post(
        "http://mlclient:5000/upload",
        files={"audio": audio_file},
        data=data,
        timeout=10,
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
    user["password"] = pbkdf2_sha256.hash(user["password"])

    if db.users.find_one({"username": user["username"]}):
        # redirect with a message
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
