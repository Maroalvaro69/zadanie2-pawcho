# Etap budowania
FROM python:3.12-slim AS builder
LABEL org.opencontainers.image.authors="Jakub Górecki"

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Etap końcowy
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY . .
EXPOSE 5000
HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1
CMD ["python", "app.py"]
