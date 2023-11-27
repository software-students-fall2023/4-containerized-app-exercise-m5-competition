"""pytest for ML"""
import os


def test_upload_without_login(ml_client):
    """test upload without login"""
    response = ml_client.post('/upload', data={'audio': 'fake_audio_data'})
    assert response.status_code == 400


def test_upload_with_login(ml_client, ml_db):
    """test upload with login"""
    user_id = '1'

    file_path = "tests/kids_are_talking.wav"
    assert os.path.exists(file_path)
    with open(file_path, "rb") as file:
        data = {"audio": (file, "file.wav"), "user_id": user_id}
        response = ml_client.post(
            "/upload", data=data, content_type="multipart/form-data"
        )
    assert response.status_code == 200

    json_data = response.get_json()
    assert 'transcript' in json_data
    assert 'sentiment' in json_data
    assert 'filename' in json_data

    collection = ml_db.db['history']
    collection.insert_one({'user_id': '1', 'transcript': json_data['transcript'],
                           'sentiment': json_data['sentiment'],
                           'filename': json_data['filename']})
    document = collection.find_one({'user_id': '1'})
    assert document is not None
    assert document['transcript'] == json_data['transcript']
    # assert document['filename'] == json_data['filename']


def test_upload_route(ml_client):
    """upload route test"""
    response = ml_client.post("/upload", data={})
    assert response.status_code == 400


def test_upload_audio(ml_client):
    """tests upload audio"""
    file_path = "tests/kids_are_talking.wav"
    assert os.path.exists(file_path)
    with open(file_path, "rb") as file:
        data = {"audio": (file, "file.wav")}
        response = ml_client.post(
            "/upload", data=data, content_type="multipart/form-data"
        )
    assert response.status_code == 200
    assert "transcript" in response.json
    assert "sentiment" in response.json


def test_upload_without_audio(ml_client):
    """tests upload without audio"""
    response = ml_client.post(
        "/upload", data={}, content_type="multipart/form-data"
    )
    assert response.status_code == 400
    assert "No audio file" in response.data.decode()


def test_upload_with_wrong_file(ml_client):
    """tests upload with wrong file"""
    file_path = "tests/file.txt"
    assert os.path.exists(file_path)
    with open(file_path, "rb") as file:
        data = {"audio": (file, "file.txt")}
        response = ml_client.post(
            "/upload", data=data, content_type="multipart/form-data"
        )
    assert response.status_code == 500


def test_ouput_of_transcribe_audio(transcribe_audio_func):
    """tests output of transcribe audio"""
    file_path = "tests/kids_are_talking.wav"
    assert os.path.exists(file_path)
    assert transcribe_audio_func(file_path) == "kids are talking by the door"
