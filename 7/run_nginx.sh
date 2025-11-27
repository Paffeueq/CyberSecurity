#!/bin/bash
# run_nginx.sh - Start Nginx server with SSL configuration

# Create logs directory if it doesn't exist
mkdir -p logs

echo "Starting Nginx server with SSL configuration..."
echo ""
echo "=== SSL Configuration ==="
echo "Certificate: ./certs/server.crt"
echo "Private Key: ./certs/server.key"
echo ""
echo "=== Server Configuration ==="
echo "HTTP Port: 80 (redirects to HTTPS)"
echo "HTTPS Port: 443"
echo "Proxy Target: 127.0.0.1:8000 (Flask/Gunicorn)"
echo ""

# Run nginx
nginx -c "$(pwd)/nginx.conf" -g "daemon off;"
