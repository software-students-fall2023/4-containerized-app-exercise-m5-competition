"""
machine learning client backend
This file contains API for the web-app backend usage
"""

import os
import subprocess
import random
import mongomock
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pymongo
from ml_client import transcribe_audio, analyze_sentiment

app = Flask(__name__)
CORS(app)  # Stop the security protection

# Use mongomock for testing, else use the real MongoClient
if os.environ.get("TESTING"):
    client = mongomock.MongoClient()
else:
    client = pymongo.MongoClient("mongodb://db:27017")

db = client["Isomorphism"]
collection = db["history"]  # ml result and metadata are stored in this collection
app.config["SECRET_KEY"] = "supersecretkey"


@app.route("/audio/<filename>")
def uploaded_file(filename):
    """
    serve the shared folder.
    This shared folder is used to store the audio files if the user is logged in
    """
    return send_from_directory("/audio_files", filename)


@app.route("/upload", methods=["POST"])
def upload_audio():
    """
    get the uploaded audio and do ML work.
    web-app's backend will call this API.
    """
    if "audio" not in request.files:
        print("No audio file in request")
        return jsonify({"error": "No audio file"}), 400
    random_number = random.randint(10000, 99999)  # generate unique file name
    audio_file = request.files["audio"]
    user_id = request.form.get("user_id", None)

    upload_dir = "audio_files"  # The shared folder
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # We only take .wav and .webm (browser mic recording) format audios
    if not audio_file.filename.lower().endswith(
        ".wav"
    ):  # If the audio is in .webm format
        temp_filename = f"{user_id}_temp.webm"
        temp_audio_path = os.path.join(upload_dir, temp_filename)
        audio_file.save(temp_audio_path)  # temp .webm file waiting for conversion
        filename = f"{user_id}_{random_number}.wav"
        audio_path = os.path.join(upload_dir, filename)
        try:
            subprocess.run(
                ["ffmpeg", "-i", temp_audio_path, audio_path], check=True
            )  # Convert the audio to .wav format
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while converting file: {e}")
        os.remove(temp_audio_path)  # remove the temp .webm file
    else:  # If the audio is already in .wav format
        filename = f"{user_id}_{random_number}.wav"
        audio_path = os.path.join(upload_dir, filename)
        audio_file.save(audio_path)  # Save the file in the shared folder

    # This is the actual machine learning work
    transcript = transcribe_audio(audio_path)  # Transcription
    sentiment = analyze_sentiment(transcript)  # Sentiment

    if user_id:  # If the user is logged in
        # Store user id, transcription, sentiment polarity, and file name in the database
        document = {
            "user_id": user_id,
            "transcript": transcript,
            "sentiment": sentiment.polarity,
            "filename": filename,
        }
        collection.insert_one(document)
        # Return transcript, sentiment, and file name
        return (
            jsonify(
                {
                    "transcript": transcript,
                    "sentiment": sentiment.polarity,
                    "filename": filename,
                }
            ),
            200,
        )

    # If user is not logged in, process the file but do not save it
    os.remove(audio_path)
    return jsonify({"transcript": transcript, "sentiment": sentiment.polarity}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
