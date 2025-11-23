from fastapi.testclient import TestClient
import pytest

from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_all():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Should at least contain one known activity from the in-memory DB
    assert "Soccer Team" in data


def test_signup_and_duplicate_signup():
    activity = "Soccer Team"
    email = "test_student@mergington.edu"

    # Ensure email not present initially
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should return 400
    resp2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp2.status_code == 400

    # Clean up
    activities[activity]["participants"].remove(email)


def test_unregister_participant():
    activity = "Basketball Club"
    email = "temp_student@mergington.edu"

    # Ensure participant is signed up
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    # Unregister
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should return 404
    resp2 = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp2.status_code == 404
