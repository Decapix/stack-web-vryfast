FROM python:3.11-slim

WORKDIR /app

# Install dependencies including wait-for-it and curl
RUN apt-get update && apt-get install -y netcat-openbsd curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Script to create initial admin user if none exists
COPY ./scripts/init_user.py /app/scripts/init_user.py
RUN chmod +x /app/scripts/init_user.py

# Create a startup script that waits for MongoDB
COPY ./scripts/start.sh /app/scripts/start.sh
RUN chmod +x /app/scripts/start.sh

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Use the startup script
CMD ["/app/scripts/start.sh"]