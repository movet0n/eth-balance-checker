import json
from web3 import Web3
from config import ADDRESSES, COLORS, ERC20_ABI, RPC_NODES


class ETHBalances:
    def __init__(self):
        self.web3_instances = {chain: Web3(Web3.HTTPProvider(node)) for chain, node in RPC_NODES.items()}

    def get_eth_balance(self, web3, address):
        balance_wei = web3.eth.get_balance(address)
        return web3.from_wei(balance_wei, "ether")

    def get_token_balance(self, web3, contract_address, wallet_address):
        contract = web3.eth.contract(address=contract_address, abi=ERC20_ABI)
        symbol = contract.functions.symbol().call()
        decimal = contract.functions.decimals().call()
        balance_wei = contract.functions.balanceOf(wallet_address).call()
        balance = balance_wei / 10**decimal
        return {"balance_wei": balance_wei, "balance": balance, "symbol": symbol, "decimal": decimal}

    def load_addresses(self):
        if ADDRESSES.endswith(".txt"):
            with open(ADDRESSES, "r") as f:
                return [line.strip() for line in f.readlines()]
        elif ADDRESSES.endswith(".json"):
            return json.load(open(ADDRESSES))
        else:
            print(f"{COLORS['RED']}Invalid file format. Please provide either .txt or .json file.{COLORS['RESET']}")
            return None

    def get_eth_balances_single_chain(self, chain):
        addresses = self.load_addresses()
        if addresses is None or chain.lower() not in self.web3_instances:
            print(f"{COLORS['RED']}\nPlease select a valid chain or correct file format\n{COLORS['RESET']}")
            return

        total_balance = 0
        eth_web3 = self.web3_instances[chain.lower()]
        for i, addr in enumerate(addresses, start=1):
            alias, address = self.parse_address(addr, i)
            balance = self.get_eth_balance(eth_web3, address)
            total_balance += balance
            print(f"{COLORS['CYAN']}>>> [{alias}]\t[{address}] {COLORS['GREEN']}{balance:.5f} ETH{COLORS['RESET']}")

        print(f"\t{COLORS['MAGENTA']}>>> TOTAL on {chain.capitalize()}: {total_balance:.5f} ETH{COLORS['RESET']}")

    def get_eth_balances_all_chains(self):
        addresses = self.load_addresses()
        if addresses is None:
            print(f"{COLORS['RED']}Invalid file format. Please provide either .txt or .json file.{COLORS['RESET']}")
            return

        total_wallets_balance = 0

        for i, addr in enumerate(addresses, start=1):
            alias, address = self.parse_address(addr, i)
            print(f"{COLORS['BLUE']}\n>>> [{alias}]\t[{address}]{COLORS['RESET']}")

            total_wallet_balance = 0
            for chain, eth_web3 in self.web3_instances.items():
                balance = self.get_eth_balance(eth_web3, address)
                total_wallet_balance += balance
                print(
                    f"\t{COLORS['BLUE']}> {COLORS['CYAN']}{chain:<10}\t{COLORS['GREEN']}{balance:.5f} ETH{COLORS['RESET']}"
                )

            total_wallets_balance += total_wallet_balance
            print(f"\t{COLORS['MAGENTA']}>>> TOTAL\t{total_wallet_balance:.5f} ETH{COLORS['RESET']}")

        print(f"\n{COLORS['YELLOW']}>>> TOTAL on these chains: {total_wallets_balance:.5f} ETH{COLORS['RESET']}")

    def parse_address(self, addr, index):
        if isinstance(addr, dict):
            return addr.get("alias", ""), addr.get("address", "")
        return index, addr
