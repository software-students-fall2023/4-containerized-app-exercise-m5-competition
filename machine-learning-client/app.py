"""ml client backend"""

import os
from flask import Flask, request, jsonify
import pymongo
from ml_client import transcribe_audio, analyze_sentiment

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://db:27017")
db = client["Isomorphism"]
collection = db["history"]
app.config["SECRET_KEY"] = "supersecretkey"


@app.route("/upload", methods=["POST"])
def upload_audio():
    """take the uploaded audio and store the result in mongodb"""
    if "audio" not in request.files:
        return "No audio file", 400

    audio_file = request.files["audio"]
    audio_path = "file.wav"
    audio_file.save(audio_path)

    transcript = transcribe_audio(audio_path)
    sentiment = analyze_sentiment(transcript)

    document = {
        "transcript": transcript,
        "sentiment": sentiment.polarity,
    }
    collection.insert_one(document)

    return jsonify({"transcript": transcript, "sentiment": sentiment}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
