import streamlit as st

from cipher_logic import (
    caesar_encrypt, caesar_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    hill_encrypt, hill_decrypt,
    rot13_encrypt, rot13_decrypt
)

def run_gui():
    st.set_page_config(page_title="Multi-Cipher Tool", layout="wide")
    st.title("🔒 Alat Multi-Cipher (Tugas 6)")
    st.markdown("Aplikasi ini mendukung enkripsi dan dekripsi menggunakan cipher klasik.")

    # --- Setup Kolom ---
    col1, col2 = st.columns(2)

    with col1:
        st.header("Input")
        operation = st.radio("Pilih Operasi:", ["Encrypt", "Decrypt"], horizontal=True)
        
        cipher_options = ["Caesar", "Vigenère", "Hill", "ROT13"]
        cipher = st.selectbox("Pilih Algoritma Cipher:", cipher_options)
        
        text_input = ""
        if operation == "Decrypt":
            uploaded_file = st.file_uploader("Atau, upload file .txt untuk dekripsi", type=["txt"])
            if uploaded_file is not None:
                text_input = uploaded_file.read().decode("utf-8")
                st.info("File berhasil dibaca. Teks ada di kotak di bawah.")
        
        text_area = st.text_area("Teks Input:", value=text_input, height=150)
        
        key = None
        if cipher == "Caesar":
            key = st.number_input("Kunci (Shift Angka):", min_value=1, max_value=25, value=3)
        elif cipher == "Vigenère":
            key = st.text_input("Kunci (Kata):", value="KUNCISAYA")
        elif cipher == "Hill":
            key = st.text_input("Kunci (4 Huruf, misal: HILL):", value="HILL", max_chars=4)
        
        # Kotak centang 'double_encrypt' muncul di kedua mode
        double_encrypt = False
        if cipher != "ROT13":
            label = "Terapkan Enkripsi Ganda (diakhiri ROT13)?" if operation == "Encrypt" else "Apakah ini hasil Enkripsi Ganda (diawali ROT13)?"
            double_encrypt = st.checkbox(label)

    with col2:
        st.header("Output")
        if st.button(f"Proses {operation}"):
            processed_text = text_area
            try:
                if operation == "Encrypt":
                    if cipher == "Caesar":
                        result = caesar_encrypt(processed_text, key)
                    elif cipher == "Vigenère":
                        result = vigenere_encrypt(processed_text, key)
                    elif cipher == "Hill":
                        result = hill_encrypt(processed_text, key)
                    elif cipher == "ROT13":
                        result = rot13_encrypt(processed_text)
                    
                    # Terapkan enkripsi ganda jika dipilih
                    if double_encrypt and cipher != "ROT13":
                        result = rot13_encrypt(result)
                        st.info("Enkripsi ganda (dengan ROT13) telah diterapkan.") 

                else: # Operation == "Decrypt"
                    if double_encrypt and cipher != "ROT13":
                        st.info("Melakukan dekripsi ganda (diawali ROT13)...")
                        processed_text = rot13_decrypt(processed_text)
                    else:
                        st.info("Melakukan dekripsi tunggal...")
                        
                    if cipher == "Caesar":
                        result = caesar_decrypt(processed_text, key)
                    elif cipher == "Vigenère":
                        result = vigenere_decrypt(processed_text, key)
                    elif cipher == "Hill":
                        result = hill_decrypt(processed_text, key)
                    elif cipher == "ROT13":
                        result = rot13_decrypt(processed_text)

                # Tampilkan Hasil
                st.subheader("Hasil:")
                st.text_area("Hasil", value=result, height=150, disabled=True, label_visibility="collapsed")
                
                st.download_button(
                    label="Unduh Hasil ke .txt",
                    data=result,
                    file_name="hasil_cipher.txt",
                    mime="text/plain"
                )

            except ValueError as e:
                st.error(f"Error: {e}")
            except Exception as e:
                st.error(f"Terjadi kesalahan tak terduga: {e}")

run_gui()