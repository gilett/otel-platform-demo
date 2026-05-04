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

def test_post_messages_publish_payload_to_kafka_topic(
        client: TestClient,
        fake_producer,
) -> None:
    import json
    from app import TOPIC
    response = client.post("/messages", json={"body": "hello world"})
    message_id = response.json()["id"]

    fake_producer.send.assert_called_once()
    call = fake_producer.send.call_args

    # Topic is the first positional argument
    assert call.args[0] == TOPIC

    # Payload is JSON-encoded bytes in the value kwarg
    value = call.kwargs["value"]
    assert isinstance(value, bytes)
    payload = json.loads(value.decode("utf-8"))
    assert payload == {"id": message_id, "body": "hello world"}

    # Ensure flush is called so the demo isn't stuck in internal buffer (Kafka handling of small payloads - batching)
    fake_producer.flush.assert_called_once()