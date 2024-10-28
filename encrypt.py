import os
import subprocess #use to run steghide
from cryptography.fernet import Fernet

def encrypt_file(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as unencrypted_file:
        plaintext = unencrypted_file.read()
    ciphertext = f.encrypt(plaintext)
    # Overwrites the same file; original file can't be recovered
    with open(filename, "wb") as encrypted_file:
        encrypted_file.write(ciphertext)

def main():
    file_name = "Text.txt"
    print("Does path exist?:", os.path.exists(file_name))
    print("If so, where?:", os.path.abspath(file_name))
    key = Fernet.generate_key()
    encrypt_file("Text.txt", key)
    print("Encryption successful!")

main()