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

def test_consume_one_processes_next_message_from_iteration() -> None:
    import json
    from unittest.mock import MagicMock

    from worker import consume_one

    fake_message = MagicMock()
    fake_message.value = json.dumps(
        {"id": "abc-123", "body": "hello"}
    ).encode("utf-8")
    iterator = iter([fake_message])

    result = consume_one(iterator, work_seconds=0)

    assert result == "abc-123"

def test_consume_one_returns_none_when_iterator_exhaused() -> None:
    from worker import consume_one

    assert consume_one(iter([]), work_seconds=0) is None