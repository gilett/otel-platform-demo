"""FastAPI application"""
from __future__ import annotations

from fastapi import FastAPI

app = FastAPI()

def get_producer():
    # Fast API will call this to get kafka producer - swap out for mock in tests.
    raise NotImplementedError("get_producer not yet implemented")

@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}