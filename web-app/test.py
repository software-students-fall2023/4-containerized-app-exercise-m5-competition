"""test for web-app"""
import os
import pytest
import requests
import app
import requests_mock


@pytest.fixture(name="global_client")
def client():
    """tests client"""
    app.app.config["TESTING"] = True
    with app.app.test_client() as global_client:
        yield global_client


def test_home_page(global_client):
    """Test the home page."""
    response = global_client.get("/")
    assert response.status_code == 200


def test_return_render_template_after_upload_audio(global_client):
    """Test return render template after upload audio."""
    file_path = "web-app/tests/kids_are_talking.wav"
    assert os.path.exists(file_path)
    with open(file_path, "rb") as file:
        data = {"audio": (file, "file.wav")}
        with requests_mock.Mocker() as m:
            m.post("http://mlclient:5000/upload", text="data")
            response = global_client.post(
                "/api/upload_audio", data=data, content_type="multipart/form-data"
            )
            assert response.status_code == 200


def test_upload_timeout(global_client):
    """Test upload timeout."""
    file_path = "web-app/tests/kids_are_talking.wav"
    assert os.path.exists(file_path)
    with open(file_path, "rb") as file:
        data = {"audio": (file, "file.wav")}
        with requests_mock.Mocker() as m:
            m.post("http://mlclient:5000/upload", exc=requests.exceptions.Timeout)
            response = global_client.post(
                "/api/upload_audio", data=data, content_type="multipart/form-data"
            )
            assert response.status_code == 408
            assert response.json == {"error": "Timeout"}
