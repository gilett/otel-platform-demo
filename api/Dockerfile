FROM python:3.12-slim

WORKDIR /app

# Install runtime deps.  The opentelemetry-bootstrap will discover packages in requirements.txt.
# From that file kafka-python-ng will pull in opentelemetry-instrumentation-kafka-python-ng automatically.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && opentelemetry-bootstrap --action=install

COPY app.py .

CMD ["opentelemetry-instrument", \
    "uvicorn", "app:app", \
    "--host", "0.0.0.0", "--port", "8000"]
