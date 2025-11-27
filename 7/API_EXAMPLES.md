# API DOCUMENTATION - EXAMPLE CALLS

## Endpoints dostępne w aplikacji Flask

### 1. Main Endpoint
```
GET /
```

**Opis**: Główny endpoint pokazujący status aplikacji, informacje o kliencie i nagłówkami proxy

**Odpowiedź**:
```json
{
  "status": "ok",
  "message": "Flask application running with Gunicorn through Nginx SSL proxy",
  "https": true,
  "client_ip": "203.0.113.42",
  "server_info": {
    "host": "localhost",
    "remote_addr": "127.0.0.1",
    "scheme": "https",
    "method": "GET"
  },
  "process_info": {
    "uid": 1000,
    "username": "user",
    "gid": 1000,
    "groups": [1000, ...],
    "current_user": "user",
    "home": "/home/user"
  },
  "headers": {
    "X-Real-IP": "203.0.113.42",
    "X-Forwarded-For": "203.0.113.42",
    "X-Forwarded-Proto": "https",
    "X-Forwarded-Host": "localhost"
  }
}
```

**Test**:
```bash
curl -k https://localhost/
```

**PowerShell**:
```powershell
Invoke-WebRequest -Uri "https://localhost/" -SkipCertificateCheck | ConvertTo-Json
```

---

### 2. Health Check
```
GET /health
```

**Opis**: Szybki health check endpoint do monitorowania

**Odpowiedź**:
```json
{
  "status": "healthy",
  "ip": "203.0.113.42"
}
```

**Test**:
```bash
curl -k https://localhost/health
```

**Częsta aktualność**: Używać do LoadBalancer health checks

---

### 3. Process Information (ZADANIE #4)
```
GET /process-info
```

**Opis**: Pokazuje uprawnienia i informacje o procesie Flask

**Odpowiedź**:
```json
{
  "message": "Current process privileges and user information",
  "uid": 1000,
  "username": "ubuntu",
  "gid": 1000,
  "groups": [1000, 27, 29, 44, 46, 114, 119, 999],
  "current_user": "ubuntu",
  "home": "/home/ubuntu"
}
```

**Test**:
```bash
curl -k https://localhost/process-info | python -m json.tool
```

**Znaczenie**:
- `uid`: User ID procesu Flask (pokazuje z jakim użytkownikiem działa)
- `username`: Nazwa użytkownika
- `gid`: Group ID
- `groups`: Dodatkowe grupy użytkownika
- `home`: Katalog domowy użytkownika

---

### 4. Client IP Detection (ZADANIE #5)
```
GET /client-ip
```

**Opis**: Pokazuje jak aplikacja widzi rzeczywisty IP klienta

**Odpowiedź**:
```json
{
  "client_ip": "203.0.113.42",
  "x_real_ip": "203.0.113.42",
  "x_forwarded_for": "203.0.113.42",
  "remote_addr": "127.0.0.1"
}
```

**Pola**:
- `client_ip`: Rzeczywisty IP klienta (po przetworzeniu ProxyFix)
- `x_real_ip`: Wartość nagłówka X-Real-IP z Nginx
- `x_forwarded_for`: Wartość nagłówka X-Forwarded-For z Nginx
- `remote_addr`: IP połączenia bezpośredniego (zawsze 127.0.0.1 przez Nginx)

**Test**:
```bash
curl -k https://localhost/client-ip
```

**Test z innego hosta**:
```bash
# Z innego komputera w sieci
curl -k https://192.168.1.100/client-ip
```

---

### 5. 404 Error Handler
```
GET /nonexistent
```

**Opis**: Test obsługi błędów 404

**Odpowiedź** (HTTP 404):
```json
{
  "error": "Not found",
  "message": "..."
}
```

**Test**:
```bash
curl -k https://localhost/nonexistent
```

---

## 🧪 Kompleksowe testy

### Bash/Linux

```bash
#!/bin/bash

# Test 1: Sprawdzenie czy server odpowiada
echo "=== Test 1: Server connectivity ==="
curl -k -I https://localhost/ | head -1

# Test 2: Process info
echo -e "\n=== Test 2: Process information ==="
curl -k https://localhost/process-info | python -m json.tool

# Test 3: Client IP detection
echo -e "\n=== Test 3: Client IP Detection ==="
curl -k https://localhost/client-ip | python -m json.tool

# Test 4: Health check
echo -e "\n=== Test 4: Health Check ==="
curl -k https://localhost/health | python -m json.tool

# Test 5: Headers inspection
echo -e "\n=== Test 5: All headers ==="
curl -k -i https://localhost/ 2>&1 | grep -E "^(HTTP|Strict|X-Frame|X-Content)"

# Test 6: HTTP redirect
echo -e "\n=== Test 6: HTTP to HTTPS redirect ==="
curl -I http://localhost/ 2>&1 | grep -E "^(HTTP|Location)"
```

### PowerShell

```powershell
# Test 1: Main endpoint
$response = Invoke-WebRequest -Uri "https://localhost/" -SkipCertificateCheck
$response.Content | ConvertFrom-Json | Format-List

# Test 2: Process information
$process = Invoke-WebRequest -Uri "https://localhost/process-info" -SkipCertificateCheck
($process.Content | ConvertFrom-Json).username

# Test 3: Client IP
$clientIp = Invoke-WebRequest -Uri "https://localhost/client-ip" -SkipCertificateCheck
$clientIp.Content | ConvertFrom-Json

# Test 4: Health check
$health = Invoke-WebRequest -Uri "https://localhost/health" -SkipCertificateCheck
$health.Content | ConvertFrom-Json
```

### Python

```python
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

BASE_URL = "https://localhost"
SESSION = requests.Session()
SESSION.verify = False

# Test 1: Main endpoint
response = SESSION.get(f"{BASE_URL}/")
print("=== Main Endpoint ===")
print(json.dumps(response.json(), indent=2))

# Test 2: Process info
response = SESSION.get(f"{BASE_URL}/process-info")
print("\n=== Process Information ===")
data = response.json()
print(f"Username: {data['username']}")
print(f"UID: {data['uid']}")
print(f"Groups: {data['groups']}")

# Test 3: Client IP detection
response = SESSION.get(f"{BASE_URL}/client-ip")
print("\n=== Client IP ===")
print(json.dumps(response.json(), indent=2))

# Test 4: Security headers
response = SESSION.head(f"{BASE_URL}/")
print("\n=== Security Headers ===")
for header in ['Strict-Transport-Security', 'X-Frame-Options', 'X-Content-Type-Options']:
    print(f"{header}: {response.headers.get(header, 'NOT SET')}")
```

---

## 📊 Response Status Codes

| Code | Status | Znaczenie |
|------|--------|-----------|
| 200 | OK | Żądanie powiodło się |
| 301 | Moved Permanently | HTTP → HTTPS redirect |
| 404 | Not Found | Endpoint nie istnieje |
| 500 | Internal Server Error | Błąd serwera |

---

## 🔐 Security Headers w Odpowiedziach

Każda odpowiedź zawiera:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

---

## ⚡ Performance

### Load Testing

```bash
# Wymaga ab (Apache Bench)
ab -n 1000 -c 10 -k https://localhost/

# Lub z wrk
wrk -t4 -c100 -d30s https://localhost/
```

---

## 🐛 Debugging

### Widać request headers:

```bash
curl -k -v https://localhost/client-ip
```

### SSL Certificate inspection:

```bash
openssl s_client -connect localhost:443 -showcerts
```

### Nginx logs:

```bash
tail -f logs/https_access.log
tail -f logs/https_error.log
```

---

## 🚀 Integration Example

### Monitorowanie systemu

```python
import requests
import time
from datetime import datetime

def health_check():
    try:
        response = requests.get(
            'https://localhost/health',
            verify=False,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"[{datetime.now()}] Status: {data['status']} | IP: {data['ip']}")
            return True
    except Exception as e:
        print(f"[{datetime.now()}] Error: {e}")
        return False

# Check every 30 seconds
while True:
    health_check()
    time.sleep(30)
```

---

## ✅ Checklist dla testowania

- [ ] HTTPS działa (port 443)
- [ ] HTTP redirect do HTTPS
- [ ] Certyfikat SSL załadowany
- [ ] Process info endpoint dostępny
- [ ] Client IP poprawnie odczytywany
- [ ] Security headers obecne
- [ ] Nginx logi zapisywane
- [ ] Gunicorn workers działają
- [ ] Brak błędów w logach
