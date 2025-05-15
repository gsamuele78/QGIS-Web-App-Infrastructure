#!/bin/bash

# Set user-specific environment
export XDG_RUNTIME_DIR=/run/user/1000
export DISPLAY=:100

# Attempt SSO authentication
python3 /home/qgis/sso_auth.py

# Check authentication status
if [ $? -eq 0 ]; then
    # Start QGIS with authenticated user context
    xpra start \
        --daemon=no \
        --start-child="qgis --norestore" \
        --exit-with-children \
        --start-via-proxy=yes \
        --html=on \
        $DISPLAY
else
    echo "SSO Authentication Failed. Exiting."
    exit 1
fi