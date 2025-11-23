# Dokumentacja Projektu: Szyfrowana Komunikacja RSA

## Spis Treści
1. [Zadanie 1A - Wiadomość do deadbeef](#zadanie-1a)
2. [Zadanie 2A - Komunikacja dwukierunkowa](#zadanie-2a)
3. [Architektura systemu](#architektura)
4. [Jak uruchomić](#jak-uruchomic)

---

## Zadanie 1A: Wysłanie zaszyfrowanej wiadomości do deadbeef {#zadanie-1a}

### Cel
Wysłać poprawnie zaszyfrowaną wiadomość do użytkownika `deadbeef` i otrzymać odszyfrowaną wiadomość w odpowiedzi.

### Jak to działa
1. **Klient** pobiera klucz publiczny `deadbeef` z serwera
2. **Klient** szyfruje wiadomość algorytmem **RSA-OAEP** kluczem publicznym
3. **Klient** koduje wiadomość w base64 i wysyła do serwera
4. **Serwer** odbiera zaszyfrowaną wiadomość
5. **Serwer** odszyfrowuje wiadomość używając **prywatnego klucza deadbeef**
6. **Serwer** zwraca odszyfrowaną wiadomość w formacie JSON

### Jak uruchomić

**Terminal 1 - SERWER:**
```powershell
cd "d:\stud\sem 5\OchronaDanych\6\rsa_server_client_with_keys\server"
$env:DEADBEEF_KEY_1 = "key.1"
$env:DEADBEEF_KEY_2 = "key.2"
python app.py
```

**Terminal 2 - KLIENT:**
```powershell
cd "d:\stud\sem 5\OchronaDanych\6"
python send_message.py
```

### Rezultat
- Klient wysyła: `"Cześć deadbeef! To jest zaszyfrowana wiadomość."`
- Serwer odszyfrowuje i zwraca tę samą wiadomość w odpowiedzi
- ✅ **SUKCES**: Otrzymanie odszyfrowanej wiadomości potwierdza poprawne wykonanie

### Pliki
- `send_message.py` - skrypt klienta dla zadania 1A

---

## Zadanie 2A: Dwukierunkowa szyfrowana komunikacja {#zadanie-2a}

### Cel
Przeprowadzić szyfrowaną komunikację w obu kierunkach między dwoma użytkownikami: `john_snow` i `bob_bob`.

### Jak to działa

#### Faza 1: Generowanie kluczy
1. **Skrypt `generate_keys.py`** generuje pary kluczy RSA (2048-bit) dla obu użytkowników
2. Każdy użytkownik otrzymuje:
   - `<username>_pub.key` - klucz publiczny
   - `<username>_priv.key` - klucz prywatny

#### Faza 2: Serwer załadowuje klucze
Serwer (`app.py`) załadowuje klucze dla trzech użytkowników:
- `deadbeef` (z zadania 1A)
- `john_snow` (nowy użytkownik)
- `bob_bob` (nowy użytkownik)

#### Faza 3: Komunikacja
```
john_snow (Nadawca)
    ↓ szyfruje wiadomość kluczem publicznym bob_bob
    ↓ wysyła do serwera
    ↓
SERWER (przechowuje zaszyfrowaną wiadomość)
    ↓
bob_bob (Odbiorca)
    ↓ pobiera wiadomość
    ↓ odszyfrowuje kluczem prywatnym bob_bob
    ↓ przeczytuje: "Cześć Bob! To ja, John Snow. Jak się masz?"
    ↓
bob_bob (Nadawca odpowiedzi)
    ↓ szyfruje odpowiedź kluczem publicznym john_snow
    ↓ wysyła do serwera
    ↓
SERWER (przechowuje zaszyfrowaną odpowiedź)
    ↓
john_snow (Odbiorca odpowiedzi)
    ↓ pobiera wiadomość
    ↓ odszyfrowuje kluczem prywatnym john_snow
    ↓ przeczytuje: "Cześć John! Dobrze się mam, dzięki!"
```

### Jak uruchomić

**Krok 1: Generowanie kluczy (tylko raz)**
```powershell
cd "d:\stud\sem 5\OchronaDanych\6"
python generate_keys.py
```

**Terminal 1 - SERWER:**
```powershell
cd "d:\stud\sem 5\OchronaDanych\6\rsa_server_client_with_keys\server"
$env:DEADBEEF_KEY_1 = "key.1"
$env:DEADBEEF_KEY_2 = "key.2"
python app.py
```

**Terminal 2 - BOB (czeka na wiadomość):**
```powershell
cd "d:\stud\sem 5\OchronaDanych\6"
python bob_bob_client.py
```

**Terminal 3 - JOHN (wysyła wiadomość):**
```powershell
cd "d:\stud\sem 5\OchronaDanych\6"
python john_snow_client.py
```

### Rezultat
- Na stronie `http://127.0.0.1:5555/` widać dwie zaszyfrowane wiadomości:
  - Wiadomość od John do Bob (zaszyfrowana)
  - Wiadomość od Bob do John (zaszyfrowana)
- John otrzymuje odszyfrowaną odpowiedź od Bob
- Bob otrzymuje odszyfrowaną wiadomość od John
- ✅ **SUKCES**: Dwukierunkowa komunikacja działa poprawnie

### Pliki
- `generate_keys.py` - generator kluczy RSA
- `john_snow_client.py` - klient dla użytkownika john_snow
- `bob_bob_client.py` - klient dla użytkownika bob_bob

---

## Architektura systemu {#architektura}

### Struktura folderów
```
d:\stud\sem 5\OchronaDanych\6\
├── rsa_server_client_with_keys/
│   ├── server/
│   │   ├── app.py              # Serwer Flask
│   │   ├── key.1               # Klucz publiczny deadbeef
│   │   ├── key.2               # Klucz prywatny deadbeef
│   │   ├── john_snow_pub.key   # Klucz publiczny john_snow
│   │   ├── john_snow_priv.key  # Klucz prywatny john_snow
│   │   ├── bob_bob_pub.key     # Klucz publiczny bob_bob
│   │   ├── bob_bob_priv.key    # Klucz prywatny bob_bob
│   │   └── templates/
│   │       └── index.html      # Strona główna serwera
│   └── client/
│       └── client.py           # Klasa klienta
├── send_message.py             # Zadanie 1A - wysyłanie do deadbeef
├── john_snow_client.py         # Zadanie 2A - klient john_snow
├── bob_bob_client.py           # Zadanie 2A - klient bob_bob
├── generate_keys.py            # Generator kluczy RSA
└── jak_ruuchomic.txt          # Instrukcje szybkie
```

### Technologie
- **Python 3.x**
- **Flask** - serwer HTTP
- **PyCryptodome** - biblioteka szyfrowania RSA
- **Base64** - kodowanie wiadomości
- **JSON** - format komunikacji

### Algorytm szyfrowania
- **RSA-OAEP** (Optimal Asymmetric Encryption Padding)
- **Rozmiar klucza**: 2048 bitów
- **Funkcja haszowania**: SHA-1 (domyślna w PKCS1_OAEP)

---

## Endpointy API serwera {#api}

### GET `/`
Wyświetla stronę główną z listą wszystkich wiadomości (zaszyfrowanych)

### GET `/key/<uid>`
Pobiera klucz publiczny dla danego użytkownika
```
Parametry: uid (string) - identyfikator użytkownika
Odpowiedź: Klucz publiczny w formacie PEM
```

### POST `/key/<uid>`
Wysyła klucz publiczny dla danego użytkownika (tylko dla nowych użytkowników)
```
Parametry: uid (string)
Body: {"key": "<public_key_in_PEM_format>"}
```

### GET `/message/<uid>`
Pobiera wiadomość dla danego użytkownika (w formacie base64)
```
Parametry: uid (string)
Odpowiedź: Wiadomość zakodowana w base64 (zaszyfrowana)
```

### POST `/message/<uid>`
Wysyła wiadomość dla danego użytkownika
```
Parametry: uid (string)
Body: {"message": "<base64_encrypted_message>"}
Odpowiedź: Potwierdzenie lub odszyfrowana wiadomość (JSON)
```

---

## Bezpieczeństwo {#bezpieczenstwo}

### Co jest zabezpieczone?
✅ Wiadomości są szyfrowane RSA-OAEP  
✅ Każdy użytkownik ma unikalną parę kluczy  
✅ Klucze prywatne nigdy nie są wysyłane  
✅ Tylko posiadacz klucza prywatnego może odszyfować wiadomość  
✅ Wiadomości są przechowywane na serwerze w formie zaszyfrowanej  

### Co NIE jest zabezpieczone?
⚠️ Połączenie HTTP (brak szyfrowania transportu) - to demo!  
⚠️ Klucze przechowywane w plikach tekstowych  
⚠️ Brak autentykacji użytkowników  
⚠️ Brak ochrony przed CSRF  

---

## Podsumowanie {#podsumowanie}

### Zadanie 1A ✅
- Wysłanie zaszyfrowanej wiadomości do deadbeef
- Otrzymanie odszyfrowanej wiadomości w odpowiedzi
- **STATUS**: ZREALIZOWANE

### Zadanie 2A ✅
- Dwukierunkowa szyfrowana komunikacja między john_snow i bob_bob
- Każda strona może odszyfować swoją wiadomość
- **STATUS**: ZREALIZOWANE

---

## Dodatkowo

### Jak sprawdzić co się dzieje?
1. Otwórz `http://127.0.0.1:5555/` w przeglądarce
2. Zobaczysz zaszyfrowane wiadomości na stronie
3. Każda wiadomość ma etykietę z adresem nadawcy

### Jak debugować?
- Sprawdź logi w terminalach (stdout)
- Każdy skrypt wypisuje kroki: pobieranie klucza, szyfrowanie, wysyłanie
- Serwer wypisuje GET/POST requesty

### Co zmienić?
- W `send_message.py`, `john_snow_client.py`, `bob_bob_client.py` zmień zmienną `MESSAGE` na inną treść
- Wiadomości będą szyfrowane i wysyłane normalna

---

**Projekt wykonany: 23.11.2025**  
**Przedmiot: Ochrona Danych**  
**Temat: RSA-OAEP Szyfrowana Komunikacja**
