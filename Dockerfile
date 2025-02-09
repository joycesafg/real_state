FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY property_friends_real_state/app/ /app
COPY docker-compose.yml .

# Default command to start everything
CMD ["docker-compose", "-f", "/app/docker-compose.yml", "up"]
