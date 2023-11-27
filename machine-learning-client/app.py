"""ml client backend"""

import os
import random
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pymongo
from ml_client import transcribe_audio, analyze_sentiment

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["Isomorphism"]
collection = db["history"]
app.config["SECRET_KEY"] = "supersecretkey"


@app.route("/audio/<filename>")
def uploaded_file(filename):
    """serve the shared folder"""
    return send_from_directory("/audio_files", filename)


@app.route("/upload", methods=["POST"])
def upload_audio():
    """get the uploaded audio and do ML work"""
    print("Audio request received")
    if "audio" not in request.files:
        print("No audio file in request")
        return jsonify({"error": "No audio file"}), 400

    audio_file = request.files["audio"]
    user_id = request.form.get("user_id", None)

    if user_id:
        upload_dir = "/audio_files"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Save the audio file only if user is logged in
        # Extract file extension and ensure it's included in the filename
        random_number = random.randint(10000, 99999)
        filename = f"{user_id}_{random_number}.wav"
        audio_path = os.path.join(upload_dir, filename)
        audio_file.save(audio_path)

        transcript = transcribe_audio(audio_path)
        sentiment = analyze_sentiment(transcript)

        # Store transcription and sentiment in the database
        document = {
            "user_id": user_id,
            "transcript": transcript,
            "sentiment": sentiment.polarity,
            "filename": filename,
        }
        print("Inserting document into database", document)
        collection.insert_one(document)

        # Return transcript, sentiment, and audio path
        return (
            jsonify(
                {
                    "transcript": transcript,
                    "sentiment": sentiment,
                    "filename": filename,  # filename with extension
                }
            ),
            200,
        )

    # If user is not logged in, process the file but do not save it
    transcript = transcribe_audio(audio_file)
    sentiment = analyze_sentiment(transcript)
    return jsonify({"transcript": transcript, "sentiment": sentiment}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
