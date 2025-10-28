import numpy as np

# ==========================================
# BAGIAN 1: FUNGSI HELPER (ALFABET & FILE)
# ==========================================

def clean_text(text):
    # Membersihkan teks: uppercase, hapus spasi, dan non-alfabet.
    return "".join(filter(str.isalpha, text)).upper()

def text_to_nums(text):
    # Mengubah teks (A-Z) menjadi list angka (0-25).
    return [ord(c) - ord('A') for c in text]

def nums_to_text(nums):
    # Mengubah list angka (0-25) kembali menjadi teks (A-Z).
    return "".join([chr(n + ord('A')) for n in nums])

def save_to_file(text, filename="output.txt"):
    # Menyimpan teks ke file.
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        return f"Berhasil disimpan ke {filename}"
    except Exception as e:
        return f"Gagal menyimpan file: {e}"

def read_from_file(filename="output.txt"):
    # Membaca teks dari file.
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: File '{filename}' tidak ditemukan."
    except Exception as e:
        return f"ERROR: Gagal membaca file: {e}"

# ==========================================
# BAGIAN 2: IMPLEMENTASI ALGORITMA CIPHER
# ==========================================

# --- 1. Caesar Cipher ---

def caesar_encrypt(plain_text, key):
    plain_text = clean_text(plain_text)
    plain_nums = text_to_nums(plain_text)
    cipher_nums = [(n + key) % 26 for n in plain_nums]
    return nums_to_text(cipher_nums)

def caesar_decrypt(cipher_text, key):
    cipher_text = clean_text(cipher_text)
    cipher_nums = text_to_nums(cipher_text)
    plain_nums = [(n - key) % 26 for n in cipher_nums]
    return nums_to_text(plain_nums)

# --- 2. Vigenère Cipher ---

def vigenere_encrypt(plain_text, key):
    plain_text = clean_text(plain_text)
    key = clean_text(key)
    if not key:
        return plain_text  # Tidak ada kunci, tidak ada enkripsi

    plain_nums = text_to_nums(plain_text)
    key_nums = text_to_nums(key)
    key_len = len(key_nums)
    cipher_nums = []

    for i, p_num in enumerate(plain_nums):
        k_num = key_nums[i % key_len]
        cipher_nums.append((p_num + k_num) % 26)
    
    return nums_to_text(cipher_nums)

def vigenere_decrypt(cipher_text, key):
    cipher_text = clean_text(cipher_text)
    key = clean_text(key)
    if not key:
        return cipher_text

    cipher_nums = text_to_nums(cipher_text)
    key_nums = text_to_nums(key)
    key_len = len(key_nums)
    plain_nums = []

    for i, c_num in enumerate(cipher_nums):
        k_num = key_nums[i % key_len]
        plain_nums.append((c_num - k_num) % 26)
        
    return nums_to_text(plain_nums)

# --- 3. Hill Cipher (2x2) ---

def mod_inv_helper(n, m):
    # Mencari modular inverse dari n mod m.
    try:
        # pow(n, -1, m) hanya berfungsi di Python 3.8+
        return pow(n, -1, m)
    except ValueError:
        return None

def create_hill_key_matrix(key):
    # Membuat matriks kunci 2x2 dari string 4 huruf.
    key = clean_text(key)
    if len(key) != 4:
        raise ValueError("Kunci Hill harus tepat 4 huruf untuk matriks 2x2.")
    nums = text_to_nums(key)
    return np.array(nums).reshape(2, 2)

def get_hill_inverse_key(K):
    # Mencari matriks inverse K mod 26.
    det = int(np.round(np.linalg.det(K))) % 26
    det_inv = mod_inv_helper(det, 26)

    if det_inv is None:
        raise ValueError(f"Matriks kunci tidak dapat di-inverse mod 26 (determinan={det}). Coba kunci lain (misal: 'GYBN').")

    # Matriks adjugate untuk 2x2
    adj = np.array([[K[1, 1], -K[0, 1]], [-K[1, 0], K[0, 0]]])
    
    # K_inv = det_inv * adj (mod 26)
    K_inv = (det_inv * adj) % 26
    return K_inv

def hill_encrypt(plain_text, key_str):
    plain_text = clean_text(plain_text)
    # Padding jika panjang ganjil
    if len(plain_text) % 2 != 0:
        plain_text += 'X'
    
    K = create_hill_key_matrix(key_str)
    # Validasi determinan sebelum enkripsi
    det = int(np.round(np.linalg.det(K))) % 26
    if mod_inv_helper(det, 26) is None:
        raise ValueError(f"Matriks kunci tidak dapat di-inverse (determinan={det}). Tidak bisa digunakan.")

    plain_nums = text_to_nums(plain_text)
    cipher_text = ""
    
    for i in range(0, len(plain_nums), 2):
        P = np.array(plain_nums[i:i+2]).reshape(2, 1) # Vektor kolom
        C = np.dot(K, P) % 26
        cipher_text += nums_to_text(C.flatten())
    
    return cipher_text

def hill_decrypt(cipher_text, key_str):
    cipher_text = clean_text(cipher_text)
    if len(cipher_text) % 2 != 0:
        raise ValueError("Ciphertext tidak valid (panjang ganjil).")

    K = create_hill_key_matrix(key_str)
    K_inv = get_hill_inverse_key(K) # Akan error jika tidak invertible
    
    cipher_nums = text_to_nums(cipher_text)
    plain_text = ""
    
    for i in range(0, len(cipher_nums), 2):
        C = np.array(cipher_nums[i:i+2]).reshape(2, 1) # Vektor kolom
        P = np.dot(K_inv, C) % 26
        plain_text += nums_to_text(P.flatten())
    
    return plain_text

# --- 4. ROT13 Cipher (untuk Enkripsi Ganda) ---

def rot13_encrypt(plain_text):
    return caesar_encrypt(plain_text, 13)

def rot13_decrypt(cipher_text):
    return caesar_decrypt(cipher_text, 13)