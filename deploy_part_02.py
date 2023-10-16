import json
from web3 import Web3
from solcx import compile_standard, install_solc
from deploy_part_01 import abi, bytecode, my_address, private_key, w3, chain_id

tx_receipt = None
nonce = None
simple_storage = None
contract_address = None


def DEPLOY():
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    global nonce
    nonce = w3.eth.get_transaction_count(my_address)
    print(nonce)
    transaction = SimpleStorage.constructor().build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce
        }
    )

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    # print(signed_txn)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Waiting for the contract to be deployed!")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Contract has been deployed!")
    print("This is the data of the transaction: ")
    print(tx_receipt)
    print(f" The contract has been deployed to {tx_receipt.contractAddress}")
    global contract_address
    contract_address = tx_receipt.contractAddress


def RETRIVE():
    global simple_storage
    simple_storage = w3.eth.contract(address=contract_address, abi=abi)
    print(f"This is the value: {simple_storage.functions.retrieve().call()}")


def STORE(value):
    global nonce
    global simple_storage
    greeting_transaction = simple_storage.functions.store(value).build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce + 1
        }
    )
    nonce = nonce + 1

    signed_greeting_tx = w3.eth.account.sign_transaction(greeting_transaction, private_key=private_key)
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_tx.rawTransaction)
    print("Updating the value ...........")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print("Value updated successfully......")
    print(tx_receipt)


DEPLOY()
RETRIVE()
STORE(15)
RETRIVE()
