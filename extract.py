import subprocess
#import wexpect


def extract_message(cover_file: str, passphrase: str) -> str:
    """
    Executes commandlines to run Steghide and obtain in order
    to obtain the "secret" message embedded within a given image.
    :param cover_file: Represents the image to be examined for a message.
    :param passphrase: The key used to decrypt and access the "secret" message
        in the image.
    :return: The text that was embedded into an image.
    """
    #extracted_file: str = ""
    extracted_file_path: str = "C:\\Users\..."

    if cover_file.endswith(".jpg"):
        if cover_file.endswith("download.jpg"):  # image containing the key
        #if cover_file == "White_shark.jpg":
            extracted_file_path += "\key.txt"
    else:  # our bmp containing encrypt.py
        extracted_file_path += "\code.txt"

    steghide_path = "C:\\Users\...\steghide-0.5.1-win32\steghide\steghide.exe"

    print("Cover file:", cover_file)
    print("File being written to:", extracted_file_path)

    #command = ["start", "cmd", "/k", steghide_path, "extract", "-sf", cover_file, "-xf", extracted_file_path]
    #command = ["start", "cmd", "/k", steghide_path, "extract", "-sf", cover_file]
    command = f'start cmd /k {steghide_path} extract -sf "{cover_file}"'
    #command = f'echo {passphrase} | "{steghide_path}" extract -sf "{cover_file}"'
    #command =["echo", passphrase, "|", steghide_path, "extract", "-sf", cover_file]

    try:
        result = subprocess.run(
            # f"start cmd /K 'steghide extract -sf {cover_file}'",
            #["cmd", "/c", command],
            command,
            input=passphrase,
            text=True,
            shell=True)
        #result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

        if cover_file.endswith(".jpg" or ".png"):
            with open(extracted_file_path, "r") as file:
                contents = file.read()
        elif cover_file.endswith(".bmp"):
            with open(extracted_file_path, "rb") as file:
                contents = file.read()
        else:
            print("Unsupported file detected!")
            return 1
        print("Extraction Successful with: " + contents)
    except FileNotFoundError as fnfe:
        print(f"The file {fnfe.filename} was not found anywhere!")
    except Exception as e:
        print(e)

    # Returns the code/key in a string format
    return contents


extract_message("download.jpg", "Mochi\n")

#extract_message("download2.bmp", "Mochi\n")
