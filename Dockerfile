# Dockerfile for AI Model Integration Module (stub)
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "api.rest_api:app", "--host", "0.0.0.0", "--port", "8000"]
