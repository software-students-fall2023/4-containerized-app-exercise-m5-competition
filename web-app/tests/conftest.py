"""Conftest for web-app"""
import pytest
from app import app as flask_app

# pylint: disable=redefined-outer-name


@pytest.fixture
def web_app_fixture():
    """Yield the Flask app for web-app testing."""
    yield flask_app


@pytest.fixture
def web_client(web_app_fixture):
    """Return a test client for the web-app Flask app."""
    return web_app_fixture.test_client()
