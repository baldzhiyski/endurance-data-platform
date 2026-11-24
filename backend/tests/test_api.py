import pytest
from fastapi.testclient import TestClient

from endurance import main


@pytest.fixture
def client():
    if not hasattr(main, "app"):
        pytest.fail("Start by defining the FastAPI application as app in main.py.", pytrace=False)
    return TestClient(main.app)


def test_health(client):
    response = client.get("/api/health")

    assert response.status_code == 200, response.text
    assert response.json() == {"status": "ok"}


def test_demo_report_matches_hand_calculated_totals(client):
    response = client.get("/api/demo/weeks")

    assert response.status_code == 200, response.text
    report = response.json()
    assert report["source"] == "synthetic"
    assert report["timezone"] == "Europe/Berlin"
    assert len(report["weeks"]) == 4
    week = report["weeks"][0]
    assert week["week_start"] == "2026-10-26"
    assert week["seconds_by_sport"] == {"run": 3300, "trail_run": 7200, "strength": 2400}
    assert [activity["source_id"] for activity in week["activities"]] == [10, 9, 8, 7]
    session = week["activities"][0]
    assert session["sport"] == "run"
    assert session["started_at"] == "2026-11-01T14:00:00+00:00"
    assert session["moving_seconds"] == 1500
    assert session["distance_meters"] == 4200.0


@pytest.mark.parametrize("timezone", ["Atlantis/Underwater", "../UTC"])
def test_invalid_timezone_yields_a_client_error(client, timezone):
    response = client.get("/api/demo/weeks", params={"timezone": timezone})

    assert response.status_code == 422
    assert "IANA timezone" in response.json()["detail"]
