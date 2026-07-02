from fastapi.testclient import TestClient

from raeburnai_executive.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_daily_briefing_endpoint():
    response = client.post("/v1/briefings/daily", json={"organisation": "TestCo"})
    assert response.status_code == 200
    body = response.json()
    assert body["organisation"] == "TestCo"
    assert body["suggested_actions"]


def test_action_execution_requires_human_approval():
    response = client.post(
        "/v1/actions/execute",
        json={"action_title": "Create board pack", "target_system": "calendar", "dry_run": True},
    )
    assert response.status_code == 428


def test_action_execution_accepts_human_approval():
    response = client.post(
        "/v1/actions/execute",
        headers={"X-Human-Approval": "approved"},
        json={"action_title": "Create board pack", "target_system": "calendar", "dry_run": True},
    )
    assert response.status_code == 200
    assert response.json()["audit_id"]
