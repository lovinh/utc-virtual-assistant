import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import streamlit as st

def encrypt_aes(plaintext):
    """
    Encrypt a plaintext string using AES CBC.
    Args:
        plaintext (str): The string to encrypt.
    Returns:
        str: The ciphertext as a Base64-encoded string.
    """
    key = base64.b64decode(st.secrets["SUPER_SECRET_KEY"])
    iv = base64.b64decode(st.secrets["SUPER_SECRET_IV"])
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(ciphertext).decode()

def decrypt_aes(ciphertext_b64):
    """
    Decrypt a ciphertext string using AES CBC.
    Args:
        ciphertext_b64 (str): The Base64-encoded ciphertext string.
    Returns:
        str: The plaintext string after decryption.
    """
    key = base64.b64decode(st.secrets["SUPER_SECRET_KEY"])
    iv = base64.b64decode(st.secrets["SUPER_SECRET_IV"])
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()
