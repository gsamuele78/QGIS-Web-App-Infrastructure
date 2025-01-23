#!/bin/bash
# File: services/qgis-desktop/start-qgis.sh

# Set display for X11
export DISPLAY=:1

# Optional: Configure SSO authentication if needed
if [ -n "$SSO_AUTH_URL" ]; then
    # Add SSO authentication logic here
    echo "Authenticating with SSO service: $SSO_AUTH_URL"
fi

# Start QGIS in the background
qgis --norestore &

# Keep container running
wait
