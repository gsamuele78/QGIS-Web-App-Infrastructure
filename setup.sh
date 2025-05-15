#!/bin/bash

# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    xpra \
    postgresql \
    postgresql-contrib \
    qgis \
    python3-qgis \
    qgis-plugin-grass

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Initialize PostgreSQL database
sudo -u postgres psql -c "CREATE DATABASE qgis_db;"
sudo -u postgres psql -c "CREATE USER qgis_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE qgis_db TO qgis_user;"

# Initialize database schema
psql -U qgis_user -d qgis_db -f config/postgres/init-users.sql

# Create required directories
mkdir -p logs/sso-auth
mkdir -p shared/qgis

# Set permissions
chmod +x start_services.py
chmod +x setup.sh