FROM python:3.11-slim

WORKDIR /app

# curl ve bash yükle (probe script için)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY healthcheck-probe.sh /usr/local/bin/healthcheck-probe.sh
RUN chmod +x /usr/local/bin/healthcheck-probe.sh

EXPOSE 8080

CMD ["python", "app.py"]

