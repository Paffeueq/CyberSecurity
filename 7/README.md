# Ochrona Danych - Serwer HTTPS z Flask i Nginx

Projekt demonstruje bezpieczną konfigurację aplikacji webowej z szyfrowanym połączeniem SSL/TLS, reverse proxy oraz prawidłowym odczytywaniem adresów IP klientów.

## 📋 Wymagania projektu

- ✅ Wygenerować certyfikat samopodpisany
- ✅ Skonfigurować Nginx do obsługi tylko połączeń HTTPS
- ✅ Użyć Nginx jako reverse proxy do aplikacji Flask
- ✅ Uruchomić Flask z serwerem WSGI (Gunicorn - nie deweloperski serwer)
- ✅ Pokazać uprawnienia procesu Flask
- ✅ Umożliwić odczytanie rzeczywistego adresu IP klienta

## 🏗️ Struktura projektu

```
.
├── app.py                      # Aplikacja Flask
├── wsgi_config.py              # Konfiguracja Gunicorn
├── nginx.conf                  # Konfiguracja Nginx z SSL
├── requirements.txt            # Zależności Python
├── generate_cert.sh            # Skrypt generowania certyfikatu
├── install_dependencies.sh     # Instalacja pakietów
├── run_flask.sh                # Uruchomienie Flask/Gunicorn
├── run_nginx.sh                # Uruchomienie Nginx
├── certs/                      # Katalog na certyfikaty SSL
│   ├── server.crt              # Certyfikat samopodpisany
│   └── server.key              # Klucz prywatny
└── logs/                       # Katalog logów
```

## 🔐 1. Generowanie certyfikatu samopodpisanego

```bash
bash generate_cert.sh
```

Genera:
- Klucz prywatny RSA 2048-bitowy: `certs/server.key`
- Certyfikat X.509 ważny 365 dni: `certs/server.crt`

```bash
# Weryfikacja certyfikatu
openssl x509 -in certs/server.crt -text -noout
```

## 🌐 2. Konfiguracja Nginx z SSL/TLS

Plik `nginx.conf` zawiera:

- **Port 80**: Automatyczne przekierowanie HTTP → HTTPS
- **Port 443**: Serwer HTTPS z reverse proxy do Flask
- **Protokoły**: TLSv1.2, TLSv1.3
- **Nagłówki bezpieczeństwa**:
  - `Strict-Transport-Security`: Wymuszenie HTTPS
  - `X-Frame-Options`: Ochrona przed clickjacking
  - `X-Content-Type-Options`: Ochrona przed MIME-sniffing

**Proxy headers dla Flask**:
```
X-Real-IP: Rzeczywisty adres IP klienta
X-Forwarded-For: Lista adresów IP (proxy chain)
X-Forwarded-Proto: Protokół (https)
X-Forwarded-Host: Host klienta
```

## 🐍 3. Aplikacja Flask z Gunicorn

### Instalacja zależności:
```bash
bash install_dependencies.sh
```

### Uruchomienie Flask z Gunicorn:
```bash
bash run_flask.sh
```

Gunicorn:
- Nasłuchuje: `127.0.0.1:8000`
- Workers: Liczba procesorów (auto)
- Timeout: 30 sekund
- Logowanie do `logs/gunicorn_*.log`

### Niepubliczny serwer:
Flask NOT serwuje bezpośrednio na porcie publicznym - tylko Nginx ma dostęp na porcie 8000.

## 👤 4. Uprawnienia procesu Flask

Aplikacja zawiera endpoint `/process-info` pokazujący:

```json
{
  "uid": 1000,
  "username": "user",
  "gid": 1000,
  "groups": [1000, ...],
  "current_user": "user",
  "home": "/home/user"
}
```

**Testowanie**:
```bash
curl -k https://localhost/process-info
```

## 🌍 5. Odczytanie rzeczywistego adresu IP

Aplikacja Flask wykorzystuje middleware `ProxyFix` z Werkzeug:

```python
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
```

Funkcja `get_client_ip()` odczytuje:
1. `X-Forwarded-For` (pierwszy IP z listy)
2. `X-Real-IP` (fallback)
3. `remote_addr` (ostateczny fallback)

**Endpoint**: `/client-ip`
```json
{
  "client_ip": "203.0.113.42",
  "x_real_ip": "203.0.113.42",
  "x_forwarded_for": "203.0.113.42",
  "remote_addr": "127.0.0.1"
}
```

## 🚀 Uruchomienie systemu

### Terminal 1 - Flask/Gunicorn:
```bash
bash run_flask.sh
```

### Terminal 2 - Nginx:
```bash
bash run_nginx.sh
```

## 🧪 Testowanie

### 1. Sprawdzenie SSL:
```bash
# HTTPS z samopodpisanym certyfikatem
curl -k https://localhost/

# Bez -k zostanie błąd (certyfikat nieznany)
curl https://localhost/
```

### 2. Redirekcja HTTP → HTTPS:
```bash
# Powinno być przekierowanie (301 lub 302)
curl -i http://localhost/
```

### 3. Informacje o procesie:
```bash
curl -k https://localhost/process-info
```

### 4. Adres IP klienta:
```bash
curl -k https://localhost/client-ip
```

### 5. Health check:
```bash
curl -k https://localhost/health
```

### 6. Testy z localhost i z innego hosta:
```bash
# Z tego samego komputera
curl -k https://127.0.0.1/client-ip

# Logowanie nginx
tail -f logs/https_access.log
```

## 📊 Monitorowanie logów

```bash
# Logi dostępu Nginx
tail -f logs/https_access.log

# Logi błędów Nginx
tail -f logs/https_error.log

# Logi Gunicorn
tail -f logs/gunicorn_access.log
tail -f logs/gunicorn_error.log
```

## 🔒 Bezpieczeństwo

- ✅ Certyfikat SSL/TLS (samo-podpisany)
- ✅ Tylko HTTPS (HTTP przekierowuje na HTTPS)
- ✅ Nagłówki bezpieczeństwa
- ✅ Flask nie publiczny (tylko poprzez Nginx)
- ✅ Gunicorn z wieloma workerami
- ✅ Prawidłowe odczytywanie IP klientów (X-Forwarded-For)

## 📝 Uwagi

1. **Certyfikat samopodpisany**: W produkcji używać certyfikaty od CA (Let's Encrypt itp.)
2. **Gunicorn vs Flask**: Flask development server nie jest dla produkcji - Gunicorn to prawidłowe rozwiązanie
3. **X-Forwarded-For**: Ważne dla reverse proxy - bez tego aplikacja widzi IP Nginxa
4. **Workers**: Automatycznie dostosowywane do liczby procesów

## 🛠️ Instalacja pakietów na systemach Linux

```bash
# Ubuntu/Debian
sudo apt-get install nginx python3-pip

# Pakiety Python (automatycznie przez install_dependencies.sh)
pip install -r requirements.txt
```

## ⚡ Szybki start

```bash
# 1. Certyfikat
bash generate_cert.sh

# 2. Zależności
bash install_dependencies.sh

# 3. Terminal 1: Flask
bash run_flask.sh

# 4. Terminal 2: Nginx
bash run_nginx.sh

# 5. Testowanie
curl -k https://localhost/
```

## 📚 Linki i referecje

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)
