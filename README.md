# Dokumentasi Tugas 6: Multi-Cipher Tool

**Kelompok:** (Chandra Yetija K., Syaddad Aulia R)
**Mata Kuliah:** MILITARY CRYPTOGRAPHY TECHONOLOGY
 
## Deskripsi Aplikasi

Aplikasi ini adalah implementasi dari berbagai algoritma cipher klasik yang dibungkus dalam dua antarmuka: GUI (Graphical User Interface) berbasis Web menggunakan Streamlit, dan CLI (Command-Line Interface) berbasis menu.

Aplikasi ini memenuhi semua persyaratan tugas, termasuk:
* Enkripsi & Dekripsi untuk 3+ algoritma.
* Pilihan menu algoritma, input teks, dan input kunci.
* Menyimpan hasil (ciphertext) ke file `.txt` dan membacanya kembali.
* Fitur pengayaan: Enkripsi Ganda (Double Encryption).

## Algoritma yang Diimplementasikan

1.  **Caesar Cipher**: Algoritma substitusi sederhana di mana setiap huruf digeser sejumlah $k$ (kunci).
2.  **Vigenère Cipher**: Algoritma substitusi polialfabetik yang menggunakan kata kunci untuk menentukan pergeseran yang berbeda-beda.
3.  **Hill Cipher**: Algoritma substitusi polialfabetik yang menggunakan aljabar linear (matriks). Implementasi ini menggunakan matriks kunci 2x2.
    * **Catatan:** Tidak semua kunci 4 huruf valid. Kunci harus membentuk matriks yang *invertible* (dapat dibalik) modulo 26. Kunci default yang aman adalah `GYBN`.
4.  **ROT13**: Kasus khusus dari Caesar Cipher dengan pergeseran 13. Algoritma ini digunakan untuk fitur "Enkripsi Ganda".

## Fitur Tambahan

### Enkripsi Ganda (Double Encryption)

Sesuai permintaan, fitur enkripsi ganda ditambahkan.
* **Saat Enkripsi:** Teks pertama-tama dienkripsi menggunakan algoritma pilihan (misal: Vigenère), kemudian hasilnya dienkripsi *lagi* menggunakan **ROT13**.
* **Saat Dekripsi:** Prosesnya dibalik. Teks pertama-tama didekripsi menggunakan **ROT13**, baru kemudian didekripsi menggunakan algoritma pilihan (misal: Vigenère).

### Penanganan File

* **GUI (Streamlit):**
    * **Simpan:** Hasil enkripsi/dekripsi dapat diunduh langsung sebagai file `hasil_cipher.txt` melalui tombol "Unduh Hasil".
    * **Baca:** Saat dekripsi, pengguna dapat mengunggah file `.txt` yang berisi ciphertext.
* **CLI (Terminal):**
    * **Simpan:** Setelah enkripsi, aplikasi akan bertanya apakah pengguna ingin menyimpan hasilnya ke `output.txt`.
    * **Baca:** Saat dekripsi, aplikasi akan bertanya apakah pengguna ingin membaca ciphertext dari `output.txt`.

## Cara Menjalankan Aplikasi

Pastikan Anda memiliki Python 3.8+ dan library yang diperlukan.

### 1. Instalasi Dependensi

Anda memerlukan `streamlit` dan `numpy`.

```bash
pip install streamlit numpy
