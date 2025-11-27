#!/bin/bash
# Generate self-signed certificate for nginx
# Valid for 365 days

CERT_DIR="./certs"
CERT_FILE="$CERT_DIR/server.crt"
KEY_FILE="$CERT_DIR/server.key"

# Create certs directory if it doesn't exist
mkdir -p "$CERT_DIR"

echo "Generating self-signed certificate..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$KEY_FILE" \
    -out "$CERT_FILE" \
    -subj "/C=PL/ST=Mazovia/L=Warsaw/O=University/CN=localhost"

echo "Certificate generated:"
echo "  Private Key: $KEY_FILE"
echo "  Certificate: $CERT_FILE"
echo ""
echo "Certificate details:"
openssl x509 -in "$CERT_FILE" -text -noout | head -20
