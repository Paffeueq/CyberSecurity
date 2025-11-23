#!/usr/bin/env python3
"""
Script dla użytkownika john_snow
Wysyła zaszyfrowaną wiadomość do bob_bob i czeka na odpowiedź
"""

import requests
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time

SERVER_URL = "http://127.0.0.1:5555"
MY_UID = "john_snow"
TARGET_UID = "bob_bob"
MY_PRIVATE_KEY_PATH = "d:\\stud\\sem 5\\OchronaDanych\\6\\rsa_server_client_with_keys\\server\\john_snow_priv.key"

def send_message_to(target_uid, message):
    """Wysyła zaszyfrowaną wiadomość do innego użytkownika"""
    
    try:
        print(f"Wysyłam wiadomość do: {target_uid}")
        
        # Pobierz klucz publiczny odbiorcy
        print(f"Pobieranie klucza publicznego {target_uid}...")
        key_response = requests.get(f"{SERVER_URL}/key/{target_uid}")
        
        if key_response.status_code != 200:
            print(f"Błąd: Nie udało się pobrać klucza. Status: {key_response.status_code}")
            return False
        
        # Zaimportuj klucz publiczny
        public_key = RSA.import_key(key_response.text)
        
        # Szyfruj wiadomość
        print(f"Szyfrowanie wiadomości: '{message}'")
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_message = cipher.encrypt(message.encode('utf-8'))
        
        # Koduj do base64
        encoded_message = base64.b64encode(encrypted_message).decode('utf-8')
        
        # Wyślij wiadomość
        print(f"Wysyłanie zaszyfrowanej wiadomości...")
        message_response = requests.post(
            f"{SERVER_URL}/message/{target_uid}",
            json={"message": encoded_message}
        )
        
        if message_response.status_code == 200:
            print(f"Wiadomość wysłana!")
            return True
        else:
            print(f"Błąd: {message_response.status_code}")
            return False
            
    except Exception as e:
        print(f"Wyjątek: {str(e)}")
        return False

def receive_and_decrypt_message():
    """Odbiera wiadomość i ją odszyfrowuje"""
    
    try:
        print(f"Pobieranie wiadomości dla: {MY_UID}...")
        response = requests.get(f"{SERVER_URL}/message/{MY_UID}")
        
        if response.status_code == 200:
            # Wiadomość jest zakodowana w base64
            encoded_msg = response.text
            encrypted_msg = base64.b64decode(encoded_msg.encode())
            
            # Załaduj mój klucz prywatny
            with open(MY_PRIVATE_KEY_PATH, 'rb') as f:
                private_key = RSA.import_key(f.read())
            
            # Odszyfruj
            decipher = PKCS1_OAEP.new(private_key)
            decrypted = decipher.decrypt(encrypted_msg)
            
            print(f"Odebrana i odszyfrowana wiadomość: {decrypted.decode('utf-8')}")
            return True
        else:
            print(f"Brak wiadomości: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Błąd przy odbiorze: {str(e)}")
        return False

if __name__ == "__main__":
    print(" === JOHN SNOW - WYSYLAM WIADOMOŚĆ ===\n")
    
    # Wysłanie wiadomości
    message = "Czesc Bob! To ja, John Snow. Jak sie masz?"
    send_message_to(TARGET_UID, message)
    
    print("\n Czekam na odpowiedź od bob_bob...")
    print("(bob_bob musi uruchomić swój skrypt)\n")
    
    # Czekaj na odpowiedź
    max_attempts = 30
    for i in range(max_attempts):
        if receive_and_decrypt_message():
            print("Komunikacja dwukierunkowa udana!")
            break
        else:
            if i < max_attempts - 1:
                print(f"Czekam... próba {i+1}/{max_attempts}")
                time.sleep(2)
