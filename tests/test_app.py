import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)
initial_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))
    yield


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    assert email not in activities[activity_name]["participants"]

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    delete_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Gym Class"
    email = "newstudent@mergington.edu"
    assert email not in activities[activity_name]["participants"]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]
