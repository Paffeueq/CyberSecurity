#!/usr/bin/env python3
"""
Skrypt do generowania par kluczy RSA dla użytkowników
"""

from Crypto.PublicKey import RSA
import os

def generate_keys_for_user(username, key_size=2048):
    """Generuje parę kluczy RSA dla użytkownika"""
    
    print(f"[*] Generuję klucze dla użytkownika: {username}")
    
    # Generuj nową parę kluczy
    key = RSA.generate(key_size)
    
    # Klucz publiczny
    public_key = key.publickey().export_key()
    # Klucz prywatny
    private_key = key.export_key()
    
    # Zapisz klucze w folderze serwera
    server_dir = "d:\\stud\\sem 5\\OchronaDanych\\6\\rsa_server_client_with_keys\\server"
    
    public_key_path = os.path.join(server_dir, f"{username}_pub.key")
    private_key_path = os.path.join(server_dir, f"{username}_priv.key")
    
    with open(public_key_path, 'wb') as f:
        f.write(public_key)
    
    with open(private_key_path, 'wb') as f:
        f.write(private_key)
    
    print(f"[+] Klucz publiczny: {public_key_path}")
    print(f"[+] Klucz prywatny: {private_key_path}")
    print()

if __name__ == "__main__":
    print("[*] === GENEROWANIE KLUCZY RSA ===\n")
    
    generate_keys_for_user("john_snow")
    generate_keys_for_user("bob_bob")
    
    print("[+] Wszystkie klucze wygenerowane!")
