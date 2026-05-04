"""FastAPI application"""
from __future__ import annotations

import json
import os
import uuid

from fastapi import FastAPI, Depends
from kafka import KafkaProducer
from pydantic import BaseModel

KAFKA_BOOTSTRAP_SERVERS = os.environ.get(
    "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
)
TOPIC = "messages"

app = FastAPI()

def get_producer() -> KafkaProducer:
    # Fast API will call this to get kafka producer - swap out for mock in tests.
    return KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

class MessageIn(BaseModel):
    body: str

@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}

@app.post("/messages")
def post_message(
    msg: MessageIn,
    producer: KafkaProducer = Depends(get_producer),
) -> dict[str, str]:
    message_id = str(uuid.uuid4())
    payload = {"id": message_id, "body": msg.body}
    producer.send(TOPIC, value=json.dumps(payload).encode("utf-8"))
    producer.flush()
    return {"id": message_id, "status": "queued"}