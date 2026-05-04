from __future__ import annotations

from fastapi.testclient import TestClient

def test_healthz_returns_ok(client: TestClient) -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

def test_post_messages_rejects_missing_body(client: TestClient) -> None:
    response = client.post("/messages", json={})
    assert response.status_code == 422

def test_post_messages_returns_id_and_queued_status(client: TestClient) -> None:
    response = client.post("/messages", json={"body": "hello"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "queued"
    assert isinstance(payload["id"], str) and len(payload["id"]) > 0