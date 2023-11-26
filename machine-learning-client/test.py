""""Tests for machine-learning-client"""
import os
import pytest
import app


@pytest.fixture(name="global_client")
def client():
    """tests client"""
    app.app.config["TESTING"] = True
    with app.app.test_client() as global_client:
        yield global_client


def test_upload_audio(global_client):
    """tests upload audio"""
    file_path = "machine-learning-client/tests/kids_are_talking.wav"
    assert os.path.exists(file_path)
    with open(file_path, "rb") as file:
        data = {"audio": (file, "file.wav")}
        response = global_client.post(
            "/upload", data=data, content_type="multipart/form-data"
        )
    assert response.status_code == 200
    assert "transcript" in response.json
    assert "sentiment" in response.json


def test_upload_without_audio(global_client):
    """tests upload without audio"""
    response = global_client.post(
        "/upload", data={}, content_type="multipart/form-data"
    )
    assert response.status_code == 400
    assert "No audio file" in response.data.decode()


def test_upload_with_wrong_file(global_client):
    """tests upload with wrong file"""
    file_path = "machine-learning-client/tests/file.txt"
    assert os.path.exists(file_path)
    with open(file_path, "rb") as file:
        data = {"audio": (file, "file.txt")}
        with pytest.raises(ValueError):
            global_client.post("/upload", data=data, content_type="multipart/form-data")
        assert ValueError(
            "Audio file could not be read as PCM WAV, "
            "AIFF/AIFF-C, or Native FLAC; check if file is corrupted or in another format"
        )


def test_ouput_of_transcribe_audio():
    """tests output of transcribe audio"""
    file_path = "machine-learning-client/tests/kids_are_talking.wav"
    assert os.path.exists(file_path)
    assert app.transcribe_audio(file_path) == "kids are talking by the door"
