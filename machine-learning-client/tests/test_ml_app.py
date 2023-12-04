"""
Tests for the webapp.
"""

import os
import pytest
from app import app


@pytest.fixture
def client():
    """
    Client fixture for test
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_upload_audio_no_file(client):
    """
    Test the /upload route without an audio file
    """
    response = client.post("/upload", data={})
    assert response.status_code == 400
    assert b"No audio file" in response.data


def test_upload_audio_with_file(client):
    """
    Test the /upload route with a valid audio file
    """
    # Path to the audio file
    audio_file_path = os.path.join("tests/test_audios", "kids_are_talking.wav")

    # Open the file in binary mode
    with open(audio_file_path, "rb") as audio_file:
        data = {"audio": (audio_file, "kids_are_talking.wav")}
        response = client.post("/upload", data=data, content_type="multipart/form-data")
        assert response.status_code == 200


def test_upload_audio_with_file_non_trancriptable(client):
    """
    Test the /upload route with an audio file that has no english words
    """
    # Path to the audio file
    audio_file_path = os.path.join("tests/test_audios", "noword.wav")

    # Open the file in binary mode
    with open(audio_file_path, "rb") as audio_file:
        data = {"audio": (audio_file, "noword.wav")}
        response = client.post("/upload", data=data, content_type="multipart/form-data")
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data.get("transcript") == "N/A"


def test_upload_audio_correctness_short_file(client):
    """
    Test the /upload route with a short audio file
    """
    # Path to the audio file
    audio_file_path = os.path.join("tests/test_audios", "kids_are_talking.wav")

    # Open the file in binary mode
    with open(audio_file_path, "rb") as audio_file:
        data = {"audio": (audio_file, "kids_are_talking.wav")}
        response = client.post("/upload", data=data, content_type="multipart/form-data")
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data.get("transcript") == "kids are talking by the door"


def test_upload_audio_correctness_long_file(client):
    """
    Test the /upload route with a long audio file
    """
    # Path to the audio file
    audio_file_path = os.path.join("tests/test_audios", "harvard.wav")

    # Open the file in binary mode
    with open(audio_file_path, "rb") as audio_file:
        data = {"audio": (audio_file, "harvard.wav")}
        response = client.post("/upload", data=data, content_type="multipart/form-data")
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data.get("transcript") == (
            "the stale smell of old beer lingers it takes heat to bring out the odor a cold dip "
            "restores health and zest a salt pickle taste fine with ham tacos al pastor are my "
            "favorite a zestful food is the hot cross bun"
        )


def test_upload_audio_with_webm_format_file(client):
    """
    Test the /upload route with a .webm short audio file
    This is to test the format conversion function of the ml backend
    """
    # Path to the audio file
    audio_file_path = os.path.join("tests/test_audios", "kids_are_talking.webm")

    # Open the file in binary mode
    with open(audio_file_path, "rb") as audio_file:
        data = {"audio": (audio_file, "kids_are_talking.webm")}
        response = client.post("/upload", data=data, content_type="multipart/form-data")
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data.get("transcript") == "kids are talking by the door"
