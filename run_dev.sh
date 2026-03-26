#!/bin/bash
set -euo pipefail

RETRY_COUNT=0
MAX_RETRIES=30
WAIT_SECONDS=2

docker-compose up -d

echo "Waiting for API..."
until curl -fsS http://localhost:8000/docs > /dev/null; do
  ((RETRY_COUNT++))
  if [ "$RETRY_COUNT" -ge "$MAX_RETRIES" ]; then
    echo "ERROR: API did not become available after $((MAX_RETRIES * WAIT_SECONDS)) seconds"
    docker-compose down || true
    exit 1
  fi
  sleep "$WAIT_SECONDS"
done

echo "Seeding data..."
docker exec -i fashion_api python scripts/seed_data.py

echo "Running tests..."
docker exec -i fashion_api python -m pytest

echo "Shutting down container..."
docker-compose down
