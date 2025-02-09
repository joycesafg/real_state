FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y docker-compose
COPY property_friends_real_state/app/ .
COPY docker-compose.yml .

# Default command to start everything
CMD ["docker-compose", "-f", "/app/docker-compose.yml", "up"]
