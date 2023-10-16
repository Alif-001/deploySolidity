import json
from web3 import Web3
from solcx import compile_standard, install_solc

install_solc("0.8.0")
print("Installation Completion")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

print(simple_storage_file)

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_code.json", "w") as file:
    json.dumps(compiled_sol)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
print('This is the bytecode ----> ')
print(bytecode)

abi = json.loads(compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"])["output"]["abi"]
print('This is the ABI ----> ')
print(abi)

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337

my_address = "0x228aF8Ea70E50C8543910710a068747134933feD"
private_key = "0x9d80ad9a65f2a2c78e8c288ce5f6d42611a8a2b67017f7f3461ac3083523b75f"
