"""ML app pytest"""

import os
import pytest
from app import app  # Moved to top-level import
from ml_defaults import USER_AUDIO

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

@pytest.fixture(name="valid_test_voice")
def fixture_valid_test_image():
    return open(USER_AUDIO / "kids_are_talking.wav", "rb")


@pytest.fixture(name="invalid_test_image")
def fixture_invalid_test_image():
    """Fixture to provide an invalid test audio."""
    return open(USER_AUDIO / "kids_are_talking.webm", "rb")


# pylint: disable=redefined-outer-name
def test_upload_audio_endpoint(app_client, valid_test_voice):
    """
    Test the /upload endpoint with an audio file.
    """
    data = {"audio": (valid_test_voice, "kids_are_talking.wav"), "user_id": "test_user"}
    response = app_client.post(
        "/upload", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == 200
    response_data = response.json
    assert "transcript" in response_data
    assert "sentiment" in response_data
    assert "filename" in response_data


# pylint: disable=redefined-outer-name
def test_upload_audio_endpoint_correctness(app_client, valid_test_voice):
    """
    Test the correctness of the /upload endpoint response.
    """
    data = {"audio": (valid_test_voice, "kids_are_talking.wav"), "user_id": "test_user"}

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
