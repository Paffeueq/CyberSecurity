#!/bin/bash
# test_deployment.sh - Comprehensive test suite for the deployment

set -e

HTTPS_URL="https://localhost"
CURL_OPTS="-k -s"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Ochrona Danych - HTTPS + Nginx + Flask Test Suite ===${NC}"
echo ""

# Wait for servers to be ready
echo "Waiting for servers to be ready..."
sleep 2

# Test 1: HTTPS connectivity
echo -e "${YELLOW}[TEST 1]${NC} HTTPS Connectivity"
if curl $CURL_OPTS $HTTPS_URL/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} HTTPS server is responding"
else
    echo -e "${RED}✗${NC} HTTPS server is NOT responding"
fi
echo ""

# Test 2: HTTP to HTTPS redirect
echo -e "${YELLOW}[TEST 2]${NC} HTTP → HTTPS Redirect"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)
if [ "$STATUS" = "301" ] || [ "$STATUS" = "302" ]; then
    echo -e "${GREEN}✓${NC} HTTP redirects to HTTPS (Status: $STATUS)"
else
    echo -e "${RED}✗${NC} HTTP redirect not working (Status: $STATUS)"
fi
echo ""

# Test 3: SSL Certificate
echo -e "${YELLOW}[TEST 3]${NC} SSL Certificate Information"
CERT_CN=$(openssl x509 -in certs/server.crt -noout -subject 2>/dev/null | grep -o "CN = [^,]*" | cut -d= -f2)
CERT_VALID=$(openssl x509 -in certs/server.crt -noout -dates 2>/dev/null | grep "notAfter")
echo -e "${GREEN}✓${NC} Certificate CN: $CERT_CN"
echo "  $CERT_VALID"
echo ""

# Test 4: Main endpoint
echo -e "${YELLOW}[TEST 4]${NC} Main Endpoint (/)"
RESPONSE=$(curl $CURL_OPTS $HTTPS_URL/)
if echo "$RESPONSE" | grep -q "Flask application running"; then
    echo -e "${GREEN}✓${NC} Main endpoint responsive"
    echo "  Response preview:"
    echo "$RESPONSE" | head -3
else
    echo -e "${RED}✗${NC} Main endpoint not working"
fi
echo ""

# Test 5: Health check
echo -e "${YELLOW}[TEST 5]${NC} Health Check Endpoint (/health)"
HEALTH=$(curl $CURL_OPTS $HTTPS_URL/health)
if echo "$HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}✓${NC} Health check passed"
    echo "  Response: $HEALTH"
else
    echo -e "${RED}✗${NC} Health check failed"
fi
echo ""

# Test 6: Process Information
echo -e "${YELLOW}[TEST 6]${NC} Process Information (/process-info)"
PROCESS_INFO=$(curl $CURL_OPTS $HTTPS_URL/process-info)
if echo "$PROCESS_INFO" | grep -q "username"; then
    echo -e "${GREEN}✓${NC} Process information available"
    USERNAME=$(echo "$PROCESS_INFO" | grep -o '"username": "[^"]*"')
    UID=$(echo "$PROCESS_INFO" | grep -o '"uid": [0-9]*')
    echo "  $USERNAME"
    echo "  $UID"
else
    echo -e "${RED}✗${NC} Process information not available"
fi
echo ""

# Test 7: Client IP Detection
echo -e "${YELLOW}[TEST 7]${NC} Client IP Detection (/client-ip)"
CLIENT_IP_INFO=$(curl $CURL_OPTS $HTTPS_URL/client-ip)
if echo "$CLIENT_IP_INFO" | grep -q "client_ip"; then
    echo -e "${GREEN}✓${NC} Client IP detection working"
    echo "  Response:"
    echo "$CLIENT_IP_INFO" | head -5
else
    echo -e "${RED}✗${NC} Client IP detection failed"
fi
echo ""

# Test 8: Security Headers
echo -e "${YELLOW}[TEST 8]${NC} Security Headers"
HEADERS=$(curl $CURL_OPTS -I $HTTPS_URL/)
if echo "$HEADERS" | grep -q "Strict-Transport-Security"; then
    echo -e "${GREEN}✓${NC} HSTS header present"
fi
if echo "$HEADERS" | grep -q "X-Frame-Options"; then
    echo -e "${GREEN}✓${NC} X-Frame-Options header present"
fi
if echo "$HEADERS" | grep -q "X-Content-Type-Options"; then
    echo -e "${GREEN}✓${NC} X-Content-Type-Options header present"
fi
echo ""

# Test 9: 404 Error handling
echo -e "${YELLOW}[TEST 9]${NC} Error Handling (404)"
ERROR_RESP=$(curl $CURL_OPTS -w "\n%{http_code}" $HTTPS_URL/nonexistent)
HTTP_CODE=$(echo "$ERROR_RESP" | tail -1)
if [ "$HTTP_CODE" = "404" ]; then
    echo -e "${GREEN}✓${NC} 404 error handling working"
else
    echo -e "${RED}✗${NC} Unexpected status code: $HTTP_CODE"
fi
echo ""

# Test 10: Logs
echo -e "${YELLOW}[TEST 10]${NC} Log Files"
if [ -f "logs/https_access.log" ]; then
    LINES=$(wc -l < logs/https_access.log)
    echo -e "${GREEN}✓${NC} Nginx access log: $LINES lines"
else
    echo -e "${YELLOW}⚠${NC} Nginx access log not found"
fi

if [ -f "logs/gunicorn_access.log" ]; then
    LINES=$(wc -l < logs/gunicorn_access.log)
    echo -e "${GREEN}✓${NC} Gunicorn access log: $LINES lines"
else
    echo -e "${YELLOW}⚠${NC} Gunicorn access log not found"
fi
echo ""

echo -e "${YELLOW}=== Test Suite Complete ===${NC}"
