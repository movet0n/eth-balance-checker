import json


ADDRESSES = "addresses/addresses.txt"


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
    "arbitrum": "https://arbitrum-one.public.blastapi.io",
    "arbitrum nova": "https://arbitrum-nova-rpc.publicnode.com",
    "base": "https://base.drpc.org",
    "ethereum": "https://rpc.payload.de",
    "linea": "https://linea.decubate.com",
    "manta": "https://1rpc.io/manta",
    "optimism": "https://optimism.drpc.org",
    "scroll": "https://scroll.drpc.org",
    "zksync": "https://zksync.drpc.org",
    "zora": "https://rpc.zora.energy",
}


with open("data/abi/erc20_abi.json") as file:
    ERC20_ABI = json.load(file)
