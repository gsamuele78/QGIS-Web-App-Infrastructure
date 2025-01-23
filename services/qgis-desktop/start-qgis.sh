#!/bin/bash
# File: services/qgis-desktop/start-qgis.sh

# Set display for X11
export DISPLAY=:1

# Attempt SSO authentication
python3 /home/qgis/sso_auth.py

# Check authentication status
if [ $? -eq 0 ]; then
    # Start QGIS with authenticated user context
    qgis --norestore &
else
    echo "SSO Authentication Failed. Exiting."
    exit 1
fi

# Keep container running
wait
