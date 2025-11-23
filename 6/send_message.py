#!/usr/bin/env python3
"""
Script do wysłania zaszyfrowanej wiadomości do użytkownika deadbeef
"""

import requests
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Konfiguracja
SERVER_URL = "http://192.168.0.57:5555"
TARGET_UID = "deadbeef"
MESSAGE = "Cześć deadbeef! To jest zaszyfrowana wiadomość."

def send_encrypted_message():
    """Wysyła zaszyfrowaną wiadomość do deadbeef"""
    
    try:
        # Krok 1: Pobierz klucz publiczny deadbeef z serwera
        print("Pobieranie klucza publicznego deadbeef z serwera...")
        key_response = requests.get(f"{SERVER_URL}/key/{TARGET_UID}")
        
        if key_response.status_code != 200:
            print(f"Błąd: Nie udało się pobrać klucza. Status: {key_response.status_code}")
            print(f"Odpowiedź: {key_response.text}")
            return False
        
        # Krok 2: Zaimportuj klucz publiczny
        print("Klucz publiczny pobrany, importowanie...")
        public_key = RSA.import_key(key_response.text)
        
        # Krok 3: Szyfruj wiadomość
        print(f"Szyfrowanie wiadomości: '{MESSAGE}'")
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_message = cipher.encrypt(MESSAGE.encode('utf-8'))
        
        # Krok 4: Koduj do base64
        print("Kodowanie zaszyfrowanej wiadomości do base64...")
        encoded_message = base64.b64encode(encrypted_message).decode('utf-8')
        
        # Krok 5: Wyślij wiadomość do serwera
        print(f"Wysyłanie zaszyfrowanej wiadomości do {TARGET_UID}...")
        message_response = requests.post(
            f"{SERVER_URL}/message/{TARGET_UID}",
            json={"message": encoded_message}
        )
        
        if message_response.status_code == 200:
            print(f"SUKCES! Odpowiedź serwera: {message_response.text}")
            
            # Krok 6: Pobierz odszyfrowaną wiadomość w odpowiedzi (jeśli serwer ją zwróci)
            response_data = message_response.json()
            if 'decrypted' in response_data:
                print(f"Odebrana odszyfrowana wiadomość: {response_data['decrypted']}")
            
            return True
        else:
            print(f"Błąd: {message_response.status_code}")
            print(f"Odpowiedź: {message_response.text}")
            return False
            
    except Exception as e:
        print(f"Wyjątek: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== WYSYŁANIE ZASZYFROWANEJ WIADOMOŚCI ===")
    print(f"Serwer: {SERVER_URL}")
    print(f"Odbiorca: {TARGET_UID}")
    print()
    
    send_encrypted_message()
