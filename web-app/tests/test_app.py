"""pytest for web-app"""


def test_home_route(web_client):
    """Test the home route."""
    response = web_client.get("/")
    assert response.status_code == 200


def test_login_route(web_client):
    """Test the login route."""
    response = web_client.get("/login")
    assert response.status_code == 200


def test_signup_route(web_client):
    """Test the signup route."""
    response = web_client.get("/signup")
    assert response.status_code == 200
