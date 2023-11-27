"""Conftest for web-app"""
from unittest.mock import Mock
import pytest
import mongomock
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


@pytest.fixture
def mocked_db():
    """Mock the database connection."""
    mock_client = mongomock.MongoClient()
    flask_app.db = mock_client.mydatabase  # 替换 Flask 应用中的 MongoDB 客户端
    yield mock_client


@pytest.fixture
def mocker():
    """Return a mocker object."""
    return Mock()
