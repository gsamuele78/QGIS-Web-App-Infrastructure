# File: services/sso-auth/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=sso_service.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the service port
EXPOSE 5000

# Run the SSO service
CMD ["flask", "run"]
