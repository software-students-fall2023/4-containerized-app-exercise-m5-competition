"""
Tests for the webapp.
"""

import os
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_upload_audio_no_file(client):
    """
    Test the /upload route without an audio file.
    """
    response = client.post("/upload", data={})
    assert response.status_code == 400
    assert b"No audio file" in response.data


def test_upload_audio_with_file(client):
    """
    Test the /upload route with an audio file.
    """
    # Path to the audio file
    audio_file_path = os.path.join("tests", "kids_are_talking.wav")

    # Open the file in binary mode
    with open(audio_file_path, "rb") as audio_file:
        data = {"audio": (audio_file, "kids_are_talking.wav")}
        response = client.post("/upload", data=data, content_type="multipart/form-data")
        assert response.status_code == 200
