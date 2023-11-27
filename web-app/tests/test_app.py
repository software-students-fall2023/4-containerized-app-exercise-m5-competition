"""pytest for web-app"""
from pymongo.collection import Collection


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


def test_signup(web_client, mocker):
    """Test the signup route."""
    # Mock the `find_one` and `insert_one` methods of the users collection
    mocker.patch.object(Collection, 'find_one', return_value=None)
    mocker.patch.object(Collection, 'insert_one', return_value=None)

    # Data to simulate a user signing up
    signup_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Make a POST request to the signup route
    response = web_client.post("/user/signup", data=signup_data)

    # Check if the response is as expected
    assert response.status_code == 302  # or other expected status code
    assert "/" in response.headers["Location"]  # check the redirect location if applicable


def test_login(web_client, mocker):
    """Test the login route."""
    # Mock the `find_one` method of the users collection
    mocker.patch.object(Collection, 'find_one', return_value=None)

    # Data to simulate a user logging in
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Make a POST request to the login route
    response = web_client.post("/user/login", data=login_data)

    # Check if the response is as expected
    assert response.status_code == 302  # or other expected status code
    assert "/" in response.headers["Location"]  # check the redirect location if applicable
