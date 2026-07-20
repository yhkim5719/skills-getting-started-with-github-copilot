from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original = deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)


client = TestClient(app_module.app)


def test_unregister_participant_removes_email_from_activity():
    signup_response = client.post(
        "/activities/Soccer Team/signup?email=student@mergington.edu"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        "/activities/Soccer Team/participants/student@mergington.edu"
    )

    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == "Unregistered student@mergington.edu from Soccer Team"
    assert "student@mergington.edu" not in app_module.activities["Soccer Team"]["participants"]


def test_unregister_participant_returns_error_when_not_found():
    response = client.delete(
        "/activities/Soccer Team/participants/unknown@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
