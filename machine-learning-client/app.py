"""ml client backend"""

import os
import uuid
import io

from flask import Flask, request, jsonify
import pymongo
from ml_client import transcribe_audio, analyze_sentiment, recognize_object

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://db:27017")
db = client["Isomorphism"]
collection = db["history"]
app.config["SECRET_KEY"] = "supersecretkey"

#Global constants
ALLOWED_PHOTO_EXTENSIONS = {'png', 'jpg', 'jpeg'}

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


@app.route("/upload_photo", methods=["POST"])
def upload_photo():
    """take the uploaded photo and store the result in MongoDB"""
    if "photo" not in request.files:
        return jsonify({"error": "No photo file"}), 400

    photo_file = request.files["photo"]

    if photo_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    photo_path = None
    if photo_file and allowed_file(photo_file.filename):
        extension = photo_file.filename.rsplit('.', 1)[1].lower()
        photo_path = os.path.join("uploads", str(uuid.uuid4()) + extension)
        photo_file.save(photo_path)

    image_binary = convert_image_to_binary(photo_path)
    result = recognize_object(photo_path);
    try:
        document = {
            "photo_binary": image_binary,
            "recognition_result": result
        }
        collection.insert_one(document)

        return jsonify({"message": "Photo uploaded successfully", "path": photo_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PHOTO_EXTENSIONS

def convert_image_to_binary(image_path):
    with open(image_path, 'rb') as image_file:
        return image_file.read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
