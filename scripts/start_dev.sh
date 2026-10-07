#!/bin/bash
# Start dev environment
set -e
echo "Starting OBSIL dev environment..."
cd infra/docker && docker compose up -d db
echo "Waiting for PostgreSQL..."
sleep 3
cd ../../backend
cp .env.example .env 2>/dev/null || true
pip install -r requirements.txt -q
alembic upgrade head
uvicorn app.main:app --reload --port 8000
