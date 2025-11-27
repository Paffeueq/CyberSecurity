# QUICK REFERENCE - OCHRONA DANYCH

## 🎯 Zadania i ich spełnienie

| # | Zadanie | Status | Lokalizacja |
|----|---------|--------|-------------|
| 1 | Wygenerować certyfikat samopodpisany | ✅ | `certs/server.{crt,key}` |
| 2 | Skonfigurować Nginx SSL/TLS (HTTPS only) | ✅ | `nginx.conf` |
| 3 | Nginx proxy do Flask + WSGI | ✅ | `nginx.conf` → `app.py` + `gunicorn` |
| 4 | Pokazać uprawnienia procesu Flask | ✅ | `/process-info` endpoint |
| 5 | Odczytanie rzeczywistego IP klienta | ✅ | `/client-ip` endpoint + `ProxyFix` |

---

## 📂 Najważniejsze pliki

```
✓ app.py                    - Flask aplikacja z odczytywaniem IP
✓ nginx.conf                - Reverse proxy + SSL/TLS
✓ wsgi_config.py            - Konfiguracja Gunicorn
✓ requirements.txt          - Python dependencies
✓ certs/server.crt          - Certyfikat SSL
✓ certs/server.key          - Klucz prywatny
```

---

## 🚀 Start - 3 kroki

### Linux/WSL:
```bash
# 1. Instalacja
bash install_dependencies.sh

# 2. Terminal 1
bash run_flask.sh

# 3. Terminal 2
bash run_nginx.sh
```

### Windows:
```cmd
# 1. Instalacja
install_dependencies.bat

# 2. Terminal 1
run_flask.bat

# 3. Terminal 2 (lub WSL)
bash run_nginx.sh
```

---

## 🧪 Testowanie (5 komend)

```bash
# 1. Główny endpoint
curl -k https://localhost/

# 2. Uprawnienia procesu (ZADANIE #4)
curl -k https://localhost/process-info

# 3. Real client IP (ZADANIE #5)
curl -k https://localhost/client-ip

# 4. Health check
curl -k https://localhost/health

# 5. Redirect test
curl -I http://localhost/
```

---

## 📋 Architektura

```
HTTPS Client :443
     ↓
  NGINX (Reverse Proxy)
  [SSL/TLS termination]
  [X-Forwarded-For headers]
     ↓
  GUNICORN :8000 (WSGI)
  [multiple workers]
     ↓
  FLASK (Web App)
  [ProxyFix middleware]
  [/process-info endpoint]
  [/client-ip endpoint]
```

---

## 🔐 Security Features

✅ TLS 1.2 + 1.3  
✅ HTTP → HTTPS redirect  
✅ HSTS header  
✅ X-Frame-Options  
✅ X-Content-Type-Options  
✅ Flask behind proxy only  
✅ Multiple Gunicorn workers  

---

## 📊 Key Endpoints

| Endpoint | Purpose | Zadanie |
|----------|---------|---------|
| `GET /` | Status + client info | Demo |
| `GET /process-info` | Process privileges | #4 |
| `GET /client-ip` | Real client IP | #5 |
| `GET /health` | Health check | Monitoring |
| `GET /*` | 404 error handling | Error handling |

---

## 🐛 Troubleshooting

| Problem | Rozwiązanie |
|---------|------------|
| Port 443 zajęty | `netstat -an \| findstr :443` → kill process |
| Certyfikat nie znaleziony | `bash generate_cert.sh` |
| Flask not responding | Check `logs/gunicorn_error.log` |
| Nginx error | Check `logs/nginx_error.log` |
| No client IP | Check `X-Forwarded-For` in `/client-ip` |

---

## 📚 Dokumentacja

- **README.md** - Pełna dokumentacja
- **WINDOWS_SETUP.md** - Instrukcje Windows
- **API_EXAMPLES.md** - Szczegółowe API calls
- **SUMMARY.md** - Podsumowanie realizacji

---

## ⚡ Poznanie systemu

1. **Przejrzyj** `nginx.conf` - widać jak działa proxy
2. **Przejrzyj** `app.py` - jak Flask odczytuje IP
3. **Sprawdź** `wsgi_config.py` - konfiguracja workersów
4. **Testuj** endpoints - zobacz response JSON-y
5. **Czytaj** logi - `tail -f logs/*.log`

---

## 🔗 Key Technologies

- **Nginx** - Reverse proxy + SSL termination
- **Flask** - Web framework
- **Gunicorn** - WSGI application server
- **OpenSSL** - Certificate generation
- **Werkzeug ProxyFix** - X-Forwarded headers handling

---

## 📝 Notes

- Certyfikat samopodpisany → dla dev/testing
- Gunicorn ≠ Flask development server (produkcja!)
- X-Forwarded-For ≠ remote_addr (z powodu proxy)
- Multiple workers = mejor performance
- Logi zawsze są w `logs/` dla debugowania

---

## ✅ Gotowe do demonstracji

Projekt zawiera:
- ✓ Działającą aplikację
- ✓ Konfiguracje na Linux i Windows
- ✓ Test suite
- ✓ Pełną dokumentację
- ✓ API documentation
- ✓ Przykłady użycia

**Wszystko jest gotowe do testowania i demonstracji!**

---

## 📞 Ostatnia weryfikacja

```bash
# Czy nginx działa?
ps aux | grep nginx

# Czy gunicorn/flask działa?
ps aux | grep gunicorn

# Czy porty nasłuchują?
netstat -tlnp | grep -E ":(80|443|8000)"

# Czy certyfikat jest OK?
openssl x509 -in certs/server.crt -noout -dates
```

---

## 🎓 Co się nauczyliśmy

1. **SSL/TLS** - samopodpisane certyfikaty
2. **Reverse Proxy** - Nginx before Flask
3. **WSGI** - Gunicorn instead of dev server
4. **Headers** - X-Forwarded-For for real IP
5. **Security** - HSTS, secure configurations
6. **Process** - Permissions and privileges
7. **Logging** - Multiple log sources

---

Last Updated: 27 Nov 2025  
Status: ✅ COMPLETED
