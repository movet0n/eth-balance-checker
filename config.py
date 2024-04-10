import json


ADDRESSES = "addresses.json"


COLORS = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "RESET": "\033[0m",
}


RPC_NODES = {
    "ethereum": "https://rpc.payload.de",
    "arbitrum": "https://1rpc.io/arb",
    "optimism": "https://optimism.drpc.org",
    "linea": "https://linea.decubate.com",
    "scroll": "https://scroll.drpc.org",
}


with open("data/abi/erc20_abi.json") as file:
    ERC20_ABI = json.load(file)
