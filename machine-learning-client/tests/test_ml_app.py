"""ML app pytest"""

import os
import pytest
from app import app  # Moved to top-level import


@pytest.fixture
def app_client():  # Renamed to avoid name clash
    """Fixture to provide Flask test client."""
    # Set TESTING environment variable
    os.environ["TESTING"] = "1"

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

    # Cleanup
    del os.environ["TESTING"]


# pylint: disable=redefined-outer-name
def test_upload_audio_endpoint(app_client):
    """
    Test the /upload endpoint with an audio file.
    """
    audio_file_path = "./tests/kids_are_talking.wav"

    with open(audio_file_path, "rb") as file:
        data = {"audio": (file, "kids_are_talking.wav"), "user_id": "test_user"}

        response = app_client.post(
            "/upload", data=data, content_type="multipart/form-data"
        )

    assert response.status_code == 200
    response_data = response.json
    assert "transcript" in response_data
    assert "sentiment" in response_data
    assert "filename" in response_data


# pylint: disable=redefined-outer-name
def test_upload_audio_endpoint_correctness(app_client):
    """
    Test the correctness of the /upload endpoint response.
    """
    audio_file_path = "./tests/kids_are_talking.wav"

    with open(audio_file_path, "rb") as file:
        data = {"audio": (file, "kids_are_talking.wav"), "user_id": "test_user"}

        response = app_client.post(
            "/upload", data=data, content_type="multipart/form-data"
        )

    assert response.status_code == 200
    response_data = response.json
    assert response_data["transcript"] == "kids are talking by the door"
    assert "sentiment" in response_data
    assert "filename" in response_data


# pylint: disable=redefined-outer-name
def test_uploaded_file_endpoint(app_client):
    """
    Test the /audio/<filename> endpoint.
    """
    test_filename = "test_audio.wav"
    test_file_path = "/audio_files/" + test_filename

    with open(test_file_path, "wb") as f:
        f.write(b"Test audio content")

    response = app_client.get(f"/audio/{test_filename}")

    assert response.status_code == 200
    assert response.data == b"Test audio content"
