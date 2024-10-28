import os
import subprocess #use to run steghide
from cryptograph.fernety import Fernet

def extract_message(image_path: string, password: string):
    pass

def main():
    bool: readyToAttack = False  # Identifies if upon execution, the computer being run from is a victim
    # Runs and continuously scans for the two pngs
    while readyToAttack is False:
        readyToAttack = os.path.exists("key.png") and os.path.exists("code.png")
    if readyToAttack:
        pass