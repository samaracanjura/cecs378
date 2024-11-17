'''#import os
#from cryptography.fernet import Fernet
#from extract import extract_file


def decrypt_file(filename: str, key: str):
    """
    Deciphers a single file provided the path of the file and the Fernet key to decrypt it.
    :param filename: Represents the file to undergo encryption
    :param key:
    :return: None
    """
    # Converts that key to a Fernet object to gain access to Fernet methods
    f_key: Fernet = Fernet(key)
    # Assigns the data inside the encrypted file to a variable
    with open(filename, "rb") as encrypted_file:
        ciphertext = encrypted_file.read()
    # Decrypts the encrypted data using the key and assigns the unencrypted data to a variable
    plaintext = f_key.decrypt(ciphertext)
    # Overwrites the encrypted file to be unencrypted once more
    with open(filename, "wb") as unencrypted_file:
        unencrypted_file.write(plaintext)


def process_directory(directory: str, key: str):
    """
    This function processes each directory, decrypting all the files in each directory. In turn will decrypt
    the .exe files to prevent potential opening and viewing of the source code in the future
    :param directory: Represents the directory that will have its files decrypted.
    :param key: Represents an instance of the Fernet Class created with a key.
    :return: None
    """
    # Unpacks the provided directory as a 3-tuple consisting of directory path, directory names, and file names
    for root, _, files in os.walk(directory):
        # Iterates through each file in the directory
        for file in files:
            # Combines the path of the directory with the file name to create the filepath of file
            file_path = os.path.join(root, file)
            # Decrypts the file given the newly generated filepath
            decrypt_file(file_path, key)
            print(file)


def main():
    with open("passphrase.txt", "r") as file:
        lines = file.readlines()
        passphrase = lines[0].strip("\n")

    # Extracts the key from a specified image
    with open("images.txt", "r") as file:
        lines = file.readlines()
        image_containing_key: str = lines[0].strip("\n")

    try:
        key_found: bool = os.path.exists(image_containing_key)
        if key_found:
            key: str = extract_file(image_containing_key, passphrase)
        else:
            raise FileNotFoundError(f"The image name/path {image_containing_key} doesn't exist in the current directory."
                                    f"Either the name fed to the variable in the code to be updated or the image "
                                    f"specified just doesn't exist.")
    except FileNotFoundError as fnfe:
        print(f"File Not Found: {fnfe}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # TODO: Update as needed
    # Should decrypt itself last in order to prevent decompiling in the future
    directories_to_decrypt = [
        #os.path.expanduser("~/Downloads"),
        #os.path.expanduser("~/Documents"),
        #os.path.expanduser("~/Pictures"),
        #os.getcwd()
    ]

    for directory in directories_to_decrypt:
        process_directory(directory, key)

    # Encrypts and removes the key from directory
    decrypt_file(image_containing_key, key)
    os.remove(image_containing_key)

    print("Decryption successful!")


main()
'''