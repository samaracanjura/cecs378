import subprocess


def extract_message(cover_file_path: str, passphrase: str):
    """
    Executes commandlines to run Steghide and obtain in order
    to obtain the "secret" message embedded within a given image.
    :param cover_file_path: Represents the path to the image to be examined for a message.
    :param passphrase: The key used to decrypt and access the "secret" message
        in the image.
    :return: The text that was embedded into the provided cover_file.
    """

    steghide_compatible_files: list[str] = ["jpeg", "jpg", "bmp", "wav", "au"]

    # TODO: Use the os module to iterate through current directory to find the pathway to steghide.exe
    steghide_path = '"steghide-0.5.1-win32\steghide\steghide.exe"'
    extracted_file: str = ""

    # Checks the compatibility of the file type with Steghide
    _, cover_file_type = cover_file_path.split(".")
    if cover_file_type not in steghide_compatible_files:
        raise TypeError("Unsupported file for Steghide detected!")

    # TODO: Change this to the name of the appropriate file
    key_file_name = "White_shark.jpg"
    code_file_name = "Greenland_Shark.bmp"

    if cover_file_path == key_file_name:
        extracted_file = "key.txt"
    elif cover_file_type == code_file_name:  # our .bmp file cone
        extracted_file = "code.txt"
    else:
        pass

    print("Cover file:", cover_file_path)
    print("File written to:", extracted_file)

    # Represents the commandline argument to be run in Command Prompt in order to extract the embedded message
    command = f'{steghide_path} extract -sf "{cover_file_path}" -p {passphrase}\n'
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
        #
        output, errors = process.communicate()

        # Checks if the file being extracted already exists
        if errors == (f'the file "{extracted_file}" does already exist. overwrite ? (y/n) steghide: could not get '
                      f'terminal attributes.\n'):
            raise Exception("NOTICE: You're attempting to overwrite a file that already exists.")
        # Checks if wrong passphrase was inputted
        elif errors == "steghide: could not extract any data with that passphrase!\n":
            raise Exception("NOTICE: Incorrect passphrase inputted")
        # The subprocess must have run without error
        else:
            # Reads the contents of the file and prints them in the console
            with open(extracted_file, "r") as file:
                contents = file.read()
                print("Extraction Successful with: " + contents)

    # Catches any errors that happen to occur
    except FileNotFoundError as fnfe:
        print(f"The file {fnfe.filename} was not found anywhere!")
        return
    except Exception as e:
        print(e)
        return

    # Returns the embedded code in a string format
    return contents


extract_message("White_shark.jpg", "Mochi")
# extract_message("Greenland_Shark.bmp", "Mochi")
