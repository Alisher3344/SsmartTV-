#!/usr/bin/env sh
# Apply migrations, then start the API. Reference data + superuser are seeded
# out-of-band (see Makefile: make seed / make superuser).
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting SsmartTv API on :8000"
exec uvicorn ssmarttv.main:app --host 0.0.0.0 --port 8000 --proxy-headers
