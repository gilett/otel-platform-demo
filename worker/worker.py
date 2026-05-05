"""Kafka queue worker"""
from __future__ import annotations

import time

def process_message(payload: dict, work_seconds: float = 0.5) -> str:
    # Sim processing a message and return message id.
    # work_seconds is parameterised so tests run instantly and function still sims a small unit of work
    message_id = payload["id"]
    if work_seconds > 0:
        time.sleep(work_seconds)
    return message_id