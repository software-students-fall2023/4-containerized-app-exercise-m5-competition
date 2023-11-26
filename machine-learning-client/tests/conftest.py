"""Conftest for ML client"""
import pytest
from app import app as ml_app

# pylint: disable=redefined-outer-name


@pytest.fixture
def ml_app_fixture():
    """Yield the Flask app for machine learning client testing."""
    yield ml_app


@pytest.fixture
def ml_client(ml_app_fixture):
    """Return a test client for the machine learning client Flask app."""
    return ml_app_fixture.test_client()
