# otel-platform-demo

End-to-end OpenTelemetry trace propogation across a aynchronous boundary:
FastAPI -> Kafka -> Python worker, with Jaeger as the backend.

Built as a deliberate practice repo - the focus is on W3C Trace context propogation through Kafka message headers, demonstrating how a single trace can span a request that crosses framework and queue boundaries.

## Status

In progress - see commits.