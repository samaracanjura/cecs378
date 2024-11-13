import subprocess


def extract_message(image_path: str, password: str) -> str:
    """
    Executes commandlines to run Steghide and obtain in order
    to obtain the "secret" message embedded within a given image.
    :param image_path: The location on the computer where the image to be
        examined is located.
    :param password: The key used to decrypt and access the "secret" message
        in the image.
    :return: A string representing the secret text from the image
    """
    if image_path == "download.jpg":
        extracted_data_file_name = "key.txt"
    else:
        extracted_data_file_name = "code.txt"

    result = subprocess.run(["steghide", "extract", "-sf", image_path, "-xf", extracted_data_file_name], input=password,
                            text=True, capture_output=True)
    with open(extracted_data_file_name, "r") as file:
        contents = file.read()
    print("Extraction Successful with: " + result.stdout)


    # Returns the code/key in a string format
    return contents