"""place-holder"""
from functools import wraps
import os
import uuid
import requests
import pymongo
from flask import Flask, request, render_template, redirect, session, jsonify
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
# Connecting to local host and same db as ml's backend
client = pymongo.MongoClient("mongodb://localhost:27017")
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
    return render_template("transcripts.html")


@app.route("/login")
def login_view():
    """Display log in page"""
    return render_template("logIn.html")


@app.route("/signup")
def signup_view():
    """Display sign up page"""
    return render_template("signUp.html")


# Form handlers


@app.route("/api/upload_audio", methods=["POST"])
def upload_audio():
    """upload audio"""
    audio_file = request.files["audio"]
    response = requests.post(
        "http://mlclient:5000/upload", files={"audio": audio_file}, timeout=5
    )
    return response.content, response.status_code


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

    # Check for existing username address
    if db.users.find_one({"username": user["username"]}):
        return jsonify({"error": "Username already in use"}), 400

    if db.users.insert_one(user):
        return start_session(user)

    return jsonify({"error": "Signup failed"}), 400


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

    return jsonify({"error": "Invalid login credentials"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
