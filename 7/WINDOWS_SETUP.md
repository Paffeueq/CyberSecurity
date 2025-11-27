# INSTRUKCJA URUCHOMIENIA NA WINDOWS

## Wstęp

Ten dokument zawiera instrukcje uruchomienia projektu na systemie Windows.

## ⚙️ Wymagania wstępne

1. **Python 3.9+**
   - Pobierz z https://www.python.org/downloads/
   - Podczas instalacji zaznacz "Add Python to PATH"

2. **OpenSSL** (do generowania certyfikatu)
   - Wersja dla Windows dostępna na https://slproweb.com/products/Win32OpenSSL.html
   - Lub użyj WSL (Windows Subsystem for Linux)

3. **Nginx** (opcjonalnie na Windows)
   - Pobierz https://nginx.org/en/download.html
   - LUB uruchom przez WSL

## 🚀 Szybki start

### 1. Przygotowanie katalogów

```cmd
mkdir certs
mkdir logs
```

### 2. Wygenerowanie certyfikatu

**Opcja A - WSL (Rekomendowana)**:
```bash
# W terminalu WSL
bash generate_cert.sh
```

**Opcja B - OpenSSL na Windows**:
```cmd
openssl req -x509 -nodes -days 365 -newkey rsa:2048 ^
    -keyout certs\server.key ^
    -out certs\server.crt ^
    -subj "/C=PL/ST=Mazovia/L=Warsaw/O=University/CN=localhost"
```

### 3. Instalacja zależności Python

```cmd
python -m pip install -r requirements.txt
```

Lub:
```cmd
install_dependencies.bat
```

### 4. Uruchomienie Flask/Gunicorn

```cmd
python -m gunicorn -c wsgi_config.py app:app
```

Lub:
```cmd
run_flask.bat
```

### 5. Uruchomienie Nginx

**Opcja A - WSL (Rekomendowana)**:
```bash
bash run_nginx.sh
```

**Opcja B - Nginx na Windows**:
```cmd
nginx -c "C:\path\to\nginx.conf"
```

## 🧪 Testowanie na Windows

### PowerShell

```powershell
# Testowanie HTTPS
Invoke-WebRequest -Uri "https://localhost/" -SkipCertificateCheck

# Process info
Invoke-WebRequest -Uri "https://localhost/process-info" -SkipCertificateCheck

# Client IP
Invoke-WebRequest -Uri "https://localhost/client-ip" -SkipCertificateCheck
```

### Command Prompt (CMD)

```cmd
REM Testowanie HTTPS z curl (wymaga curl.exe)
curl -k https://localhost/

REM Process info
curl -k https://localhost/process-info
```

### Python

```python
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

response = requests.get('https://localhost/process-info', verify=False)
print(response.json())
```

## 📋 Alternatywy na Windows

### 1. Nginx w WSL2

```bash
# W terminalu WSL
sudo apt-get install nginx
bash run_nginx.sh
```

### 2. Docker

```cmd
docker-compose up
```

(Wymaga docker-compose.yml)

### 3. Python http.server (tymczasowo)

```cmd
python -m http.server 8000
```

(Tylko do testów - nie dla produkcji!)

## 🔧 Konfiguracja Nginx na Windows

Edytuj `nginx.conf` i ustaw:
```nginx
error_log  ./logs/error.log warn;
access_log ./logs/access.log main;

# Windows paths (zmień na rzeczywiste ścieżki)
ssl_certificate "./certs/server.crt";
ssl_certificate_key "./certs/server.key";
```

## 💡 Wskazówki dla Windows

1. **Ścieżki**: Użyj `/` lub `\\` zamiast `\` w konfiguracji
2. **Porty**: Upewnij się że porty 80, 443, 8000 są dostępne
3. **Zapora sieciowa**: Dodaj wyjątek w Windows Defender Firewall
4. **Administrator**: Niektóre operacje wymagają uruchomienia jako Administrator

## 🌐 Firewall (jeśli wymagane)

```cmd
REM Otwarcie portu 443 (Administrator)
netsh advfirewall firewall add rule name="Nginx HTTPS" dir=in action=allow protocol=tcp localport=443

REM Otwarcie portu 8000 (Administrator)
netsh advfirewall firewall add rule name="Gunicorn" dir=in action=allow protocol=tcp localport=8000
```

## 🐛 Debugging

### Sprawdzenie portów

```cmd
netstat -ano | findstr :443
netstat -ano | findstr :8000
```

### Procesy

```cmd
tasklist | findstr nginx
tasklist | findstr python
```

## ⚠️ Uwagi

- Nginx na Windows ma inne zachowanie niż na Linux
- WSL2 jest rekomendowanym podejściem dla pełnej kompatybilności
- Samopodpisane certyfikaty będą dawać ostrzeżenia w przeglądarkach

## 📞 Pomoc

Jeśli napotkasz problemy:

1. Sprawdź logi w `logs/`
2. Upewnij się że porty nie są zajęte
3. Sprawdź czy Python ma dostęp do certyfikatów
4. Spróbuj uruchomić jako Administrator
