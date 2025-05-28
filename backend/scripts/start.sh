#!/bin/bash
set -e

# Parse MongoDB host and port from MONGODB_URL
if [[ -z "${MONGODB_URL}" ]]; then
    MONGODB_HOST=mongodb
    MONGODB_PORT=27017
else
    # Extract host and port from MONGODB_URL
    MONGODB_HOST=$(echo $MONGODB_URL | sed -e 's/^.*\/\///' -e 's/:.*$//' -e 's/\/.*$//')
    MONGODB_PORT=$(echo $MONGODB_URL | sed -e 's/^.*://' -e 's/\/.*$//' | grep -o '[0-9]*')
    
    # Use default port if not specified
    if [[ -z "${MONGODB_PORT}" ]]; then
        MONGODB_PORT=27017
    fi
fi

echo "Waiting for MongoDB at ${MONGODB_HOST}:${MONGODB_PORT}..."

# Wait for MongoDB to be ready
until nc -z ${MONGODB_HOST} ${MONGODB_PORT}; do
    echo "MongoDB is unavailable - sleeping"
    sleep 1
done

echo "MongoDB is up - continuing"

# Create initial admin user
echo "Running user initialization script..."
python scripts/init_user.py

# Start the FastAPI application
echo "Starting FastAPI application..."
python main.py