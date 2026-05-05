FROM python:3.12-slim

WORKDIR = /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && opentelemetry-bootstrap --action=install

COPY worker.py .

CMD ["opentelemetry-instrument", "python", "worker.py"]