"""Kafka queue worker"""
from __future__ import annotations

import time
import json
import os
from typing import Iterator

from kafka import KafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = os.environ.get(
    "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
)
TOPIC = "messages"
GROUP_ID = "worker"

def process_message(payload: dict, work_seconds: float = 0.5) -> str:
    # Sim processing a message and return message id.
    # work_seconds is parameterised so tests run instantly and function still sims a small unit of work
    message_id = payload["id"]
    if work_seconds > 0:
        time.sleep(work_seconds)
    return message_id

def consume_one(messages_iter: Iterator, work_seconds: float = 0.5) -> str | None:
    #Pop the next messages from an iterator and process it.
    # Returns the processed message id or None when the iterator is exhausted.
    # Designed to take the live KafkaConsumer iterator in production and a list iterator in tests
    # The Otel kafka-python instrumentation wraps the consumer's __next__,
    # so context extraction happens at iteration time.
    try:
        message = next(messages_iter)
    except StopIteration:
        return None
    payload = json.loads(message.value.decode("utf-8"))
    return process_message(payload, work_seconds=work_seconds)

def main() -> None:
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_rest="earliest",
    )
    print(
        f"worker connect to {KAFKA_BOOTSTRAP_SERVERS}, "
        f"watching topic {TOPIC!r} as {GROUP_ID!r}",
        flush=True
    )
    for message in consumer:
        payload = json.loads(message.value.decode("utf-8"))
        message_id = process_message(payload)
        print(f"Processed {message_id}", flush=TRUE)

if __name__ == "__main__":
    main()