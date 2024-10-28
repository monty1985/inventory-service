#!/bin/sh
set -e

# Run any necessary database migrations (if needed)
echo "Running DB migrations..."
/app/scripts/init-db.sh

# Start the FastAPI server
echo "Starting the FastAPI server..."
exec uvicorn src.main.main:app --host 0.0.0.0 --port 8000 --reload
