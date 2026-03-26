#!/bin/bash

docker-compose up -d

echo "Waiting for API..."
until curl -s http://localhost:8000/docs > /dev/null; do
  sleep 2
done

echo "Seeding data..."
python scripts/seed_data.py

echo "Running tests..."
pytest