import pymongo
from flask import Flask, request, render_template, redirect
import os

app = Flask(__name__)

# Connecting to local host
connection = pymongo.MongoClient("mongodb://localhost:27017")
db = connection["test_database"]


if __name__ == "__main__":
    PORT = os.getenv(
        "PORT", 5000
    )  # use the PORT environment variable, or default to 5000
    app.run(port=PORT)
