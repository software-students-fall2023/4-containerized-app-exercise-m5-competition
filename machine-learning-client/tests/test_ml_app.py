"""pytest for ML"""


def test_upload_route(ml_client):
    """upload route test"""
    response = ml_client.post("/upload", data={})
    assert response.status_code == 400
