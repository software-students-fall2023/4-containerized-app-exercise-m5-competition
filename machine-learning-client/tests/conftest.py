"""Conftest for ML client"""
import pytest
from app import app as ml_app, db
from ml_client import transcribe_audio


# pylint: disable=redefined-outer-name

@pytest.fixture
def ml_app_fixture():
    """Yield the Flask app for machine learning client testing."""
    yield ml_app


@pytest.fixture
def ml_client(ml_app_fixture):
    """Return a test client for the machine learning client Flask app."""
    return ml_app_fixture.test_client()


@pytest.fixture
def ml_db():
    """Return a test client for the machine learning client Flask app."""
    return db


@pytest.fixture
def transcribe_audio_func():
    """Return a mocker object."""
    return transcribe_audio
