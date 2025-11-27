#!/bin/bash
# run_flask.sh - Start Flask application with Gunicorn WSGI server

# Create logs directory if it doesn't exist
mkdir -p logs

echo "Starting Flask application with Gunicorn..."
echo ""
echo "=== Process Information ==="
echo "User: $(whoami)"
echo "UID: $(id -u)"
echo "GID: $(id -g)"
echo "Current Directory: $(pwd)"
echo ""
echo "=== Gunicorn Configuration ==="
echo "Binding: 127.0.0.1:8000"
echo "Workers: $(nproc 2>/dev/null || echo 'auto')"
echo ""

# Start Gunicorn with the Flask application
gunicorn -c wsgi_config.py app:app
