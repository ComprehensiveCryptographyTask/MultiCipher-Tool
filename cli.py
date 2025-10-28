# File: cli.py
import sys
from cipher_logic import (
    caesar_encrypt, caesar_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    hill_encrypt, hill_decrypt,
    rot13_encrypt, rot13_decrypt,
    save_to_file, read_from_file,
    clean_text
)

# Marker Dihapus

def run_cli():
    """Menjalankan antarmuka CLI berbasis menu."""
    print("="*40)
    print(" Selamat Datang di Multi-Cipher Tool (CLI) ")
    print("="*40)
    
    file_name = "output.txt" 

    while True:
        print("\n--- MENU UTAMA ---")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Keluar")
        op = input("Pilih operasi (1-3): ")

        if op == '3':
            print("Terima kasih telah menggunakan alat ini. Sampai jumpa!")
            sys.exit() 
        if op not in ['1', '2']:
            print("Pilihan tidak valid.")
            continue
        
        operation = "Encrypt" if op == '1' else "Decrypt"

        print("\n--- PILIH ALGORITMA ---")
        print("1. Caesar")
        print("2. Vigenère")
        print("3. Hill (2x2)")
        print("4. ROT13")
        ciph = input("Pilih algoritma (1-4): ")
        
        if ciph not in ['1', '2', '3', '4']:
            print("Pilihan tidak valid.")
            continue
        
        cipher_map = {'1': 'Caesar', '2': 'Vigenère', '3': 'Hill', '4': 'ROT13'}
        cipher = cipher_map[ciph]
        
        text = ""
        if operation == "Decrypt":
            load = input(f"Baca ciphertext dari file '{file_name}'? (y/n): ").lower()
            if load == 'y':
                text = read_from_file(file_name)
                if text.startswith("ERROR:"):
                    print(text)
                    continue
                print(f"Teks dibaca: {text}")
            else:
                text = input("Masukkan Ciphertext: ")
        else:
            text = input("Masukkan Plaintext: ")

        key = None
        try:
            if cipher == "Caesar":
                key = int(input("Masukkan Kunci (Shift Angka): "))
            elif cipher == "Vigenère":
                key = input("Masukkan Kunci (Kata): ")
            elif cipher == "Hill":
                key = input("Masukkan Kunci (4 Huruf, misal: HILL): ")
                if len(clean_text(key)) != 4:
                    print("Error: Kunci Hill harus 4 huruf.")
                    continue
        except ValueError:
            print("Input kunci tidak valid.")
            continue
            
        # --- LOGIKA BARU ---
        # Pertanyaan 'double' muncul di kedua mode
        double = False
        if cipher != "ROT13":
            if operation == "Encrypt":
                double = input("Terapkan Enkripsi Ganda (dengan ROT13)? (y/n): ").lower() == 'y'
            else: # Decrypt
                double = input("Apakah ini hasil Enkripsi Ganda (dekripsi ROT13 dulu)? (y/n): ").lower() == 'y'

        # --- LOGIKA PROSES BARU ---
        try:
            result = ""
            if operation == "Encrypt":
                if cipher == 'Caesar': result = caesar_encrypt(text, key)
                if cipher == 'Vigenère': result = vigenere_encrypt(text, key)
                if cipher == 'Hill': result = hill_encrypt(text, key)
                if cipher == 'ROT13': result = rot13_encrypt(text)
                
                # Terapkan enkripsi ganda jika dipilih
                if double:
                    result = rot13_encrypt(result)
                    # HANYA NOTIFIKASI
                    print("Info: Enkripsi ganda (dengan ROT13) telah diterapkan.")
                    
            else: # Decrypt
                # Balik urutan HANYA JIKA DIPILIH
                if double:
                    print("Info: Melakukan dekripsi ganda (diawali ROT13)...")
                    text = rot13_decrypt(text)
                else:
                    print("Info: Melakukan dekripsi tunggal...")
                
                if cipher == 'Caesar': result = caesar_decrypt(text, key)
                if cipher == 'Vigenère': result = vigenere_decrypt(text, key)
                if cipher == 'Hill': result = hill_decrypt(text, key)
                if cipher == 'ROT13': result = rot13_decrypt(text)

            print("\n--- HASIL ---")
            print(f"Hasil {operation}: {result}")
            
            if operation == "Encrypt":
                save = input(f"Simpan hasil ke file '{file_name}'? (y/n): ").lower()
                if save == 'y':
                    status = save_to_file(result, file_name)
                    print(status)
                    
        except Exception as e:
            print(f"\n[ERROR] Terjadi kesalahan: {e}")

# Jalankan CLI
if __name__ == "__main__":
    run_cli()