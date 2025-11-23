#!/usr/bin/env python3
"""
Deszyfracja CTF - dekodowanie obrazu PNG z ciphertextu z diakrytykami.
"""

import base64
import re
import unicodedata
from itertools import product
from pathlib import Path


class CipherDecryptor:
    """Obsługuje deszyfrację ciphertextu z diakrytykami."""
    
    PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
    
    def __init__(self):
        self.symbols = self._build_alphabet("A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z")
        self.symbols += self._build_alphabet("a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z")
        self.symbols += self._build_alphabet("0,1,2,3,4,5,6,7,8,9,+,/,=")
        
        self.scream = self._build_alphabet("A,Ȧ,A̧,A̱,Á,A̮,A̋,A̰,Ả,A̓,Ạ,Ă,Ǎ,Â,Å,A̯,A̤,Ȃ,Ã,Ā,Ä,À,Ȁ,A̽,A̦,Ⱥ")
        self.scream += self._build_alphabet("a,ȧ,a̧,a̱,á,a̮,a̋,a̰,ả,a̓,ạ,ă,ǎ,â,å,a̯,a̤,ȃ,ã,ā,ä,à,ȁ,a̽,a̦,ⱥ")
        self.scream += self._build_alphabet("0,1,2,3,4,5,6,7,8,9,ą,ḁ,æ")
        
        self.shift_mod = len(self.scream)
        self.dec_maps = self._precompute_decodings()
    
    @staticmethod
    def _build_alphabet(csv_string: str) -> list:
        """Konwertuje string CSV na listę znaków."""
        return csv_string.split(",")
    
    def _precompute_decodings(self) -> list:
        """Precompute all decoding maps for shifts 0-63."""
        maps = []
        for shift in range(64):
            rotated = self.scream[shift:] + self.scream[:shift]
            dec_map = {rotated[j]: self.symbols[j] for j in range(self.shift_mod)}
            maps.append(dec_map)
        return maps
    
    def tokenize(self, text: str) -> list:
        """
        Dzieli tekst na tokeny (znaki bazowe + diakrytyki).
        Ignoruje białe znaki.
        """
        tokens = []
        current = ""
        
        for ch in text:
            if ch.isspace():
                continue
            
            if unicodedata.combining(ch):
                if not current:
                    raise ValueError(f"Combining char bez znaku bazowego: {repr(ch)}")
                current += ch
            else:
                if current:
                    tokens.append(current)
                current = ch
        
        if current:
            tokens.append(current)
        
        # Walidacja
        scream_set = set(self.scream)
        for i, token in enumerate(tokens):
            if token not in scream_set:
                raise ValueError(f"Token spoza alfabetu na pozycji {i}: {repr(token)}")
        
        return tokens
    
    def decrypt_with_shifts(self, tokens: list, shifts: tuple, limit: int = None) -> str:
        """Deszyfruje tokeny przy znanych przesunięciach (A, B, C, D)."""
        if limit:
            tokens = tokens[:limit]
        
        result = []
        A, B, C, D = shifts
        maps = (self.dec_maps[A], self.dec_maps[B], self.dec_maps[C], self.dec_maps[D])
        
        for i, token in enumerate(tokens):
            dec_map = maps[i % 4]
            if token not in dec_map:
                raise ValueError(f"Brak mapowania dla {repr(token)}")
            result.append(dec_map[token])
        
        return "".join(result)
    
    def find_correct_shifts(self, tokens: list) -> tuple:
        """Brute force po A, B, C, D - szuka pierwszego match'a z PNG magic."""
        test_count = min(len(tokens), 12)
        
        for A, B, C, D in product(range(64), repeat=4):
            shifts = (A, B, C, D)
            try:
                b64_part = self.decrypt_with_shifts(tokens, shifts, limit=test_count)
                raw = base64.b64decode(b64_part, validate=True)
                
                if raw.startswith(self.PNG_MAGIC):
                    return shifts
            except Exception:
                continue
        
        raise RuntimeError("Nie znaleziono poprawnych przesunięć")


def main():
    """Główny workflow deszyfracji."""
    
    print("[*] Inicjalizacja deszyfracji...")
    decryptor = CipherDecryptor()
    
    # Wczytanie ciphertextu
    cipher_path = Path("1.txt")
    if not cipher_path.exists():
        print(f"[!] Plik {cipher_path} nie istnieje!")
        return
    
    ciphertext = cipher_path.read_text(encoding="utf-8")
    print(f"[+] Wczytano ciphertext ({len(ciphertext)} znaków)")
    
    # Tokenizacja
    try:
        tokens = decryptor.tokenize(ciphertext)
        print(f"[+] Tokenizacja: {len(tokens)} tokenów")
    except Exception as e:
        print(f"[!] Błąd tokenizacji: {e}")
        return
    
    # Szukanie przesunięć
    print("[*] Szukanie przesunięć A, B, C, D...")
    try:
        shifts = decryptor.find_correct_shifts(tokens)
        print(f"[+] Znaleziono: A={shifts[0]}, B={shifts[1]}, C={shifts[2]}, D={shifts[3]}")
    except RuntimeError as e:
        print(f"[!] {e}")
        return
    
    # Pełna deszyfracja
    try:
        b64_full = decryptor.decrypt_with_shifts(tokens, shifts)
        print(f"[+] Base64: {len(b64_full)} znaków")
    except Exception as e:
        print(f"[!] Błąd deszyfracji: {e}")
        return
    
    # Dekodowanie PNG
    try:
        png_data = base64.b64decode(b64_full, validate=True)
        print(f"[+] Zdekodowano: {len(png_data)} bajtów PNG")
    except Exception as e:
        print(f"[!] Błąd dekodowania base64: {e}")
        return
    
    # Zapis PNG
    output_path = Path("output.png")
    output_path.write_bytes(png_data)
    print(f"[+] PNG zapisane: {output_path}")
    
    # Szukanie flagi
    match = re.search(rb"PW\{[^}]+\}", png_data)
    if match:
        flag = match.group(0).decode('ascii', errors='ignore')
        print(f"[+] FLAGA: {flag}")
    else:
        print("[!] Nie znaleziono flagi w formacie PW{...}")


if __name__ == "__main__":
    main()