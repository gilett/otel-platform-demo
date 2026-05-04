"""Tests for the worker module."""
from __future__ import annotations

def test_process_message_returns_id_from_payload() -> None:
    from worker import process_message

    payload = {"id": "abc-123", "body": "hello"}
    assert process_message(payload, work_seconds=0) == "abc-123"

def test_process_message_raises_on_missing_id() -> None:
    import pytest

    from worker import process_message

    with pytest.raises(KeyError):
        process_message({"body": "no id"}, work_seconds=0)
