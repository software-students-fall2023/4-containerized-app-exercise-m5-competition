"""place-holder"""

import os
import pymongo
from flask import Flask


app = Flask(__name__)

# Connecting to local host
connection = pymongo.MongoClient("mongodb://localhost:27017")
db = connection["test_database"]


if __name__ == "__main__":
    PORT = int(os.getenv("PORT", "5000"))  # 5000 or default port
    app.run(port=PORT)
