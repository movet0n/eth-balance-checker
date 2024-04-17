from decimal import Decimal
import json
import math
import pandas as pd
import tabulate
from web3 import Web3
from config import ADDRESSES, COLORS, ERC20_ABI, RPC_NODES
from tokens import TOKENS


class ETHBalances:
    def __init__(self):
        self.web3_instances = {chain: Web3(Web3.HTTPProvider(node)) for chain, node in RPC_NODES.items()}

    def _load_addresses(self):
        if ADDRESSES.endswith(".txt"):
            with open(ADDRESSES, "r") as f:
                return [line.strip() for line in f.readlines()]
        elif ADDRESSES.endswith(".json"):
            return json.load(open(ADDRESSES))
        else:
            print(f"{COLORS['RED']}Invalid file format. Please provide either .txt or .json file.{COLORS['RESET']}")
            return None

    def _parse_address(self, addr: str, index: int):
        if isinstance(addr, dict):
            return addr.get("alias", ""), addr.get("address", "")
        else:
            return index, addr

    def _round_decimals_down(self, number: float, decimals: int = 2):
        factor = 10**decimals
        return math.floor(number * factor) / factor

    def get_eth_balance(self, web3, address: str):
        balance_wei = web3.eth.get_balance(address)
        return web3.from_wei(balance_wei, "ether")

    def get_token_balance(self, web3, contract_address: str, wallet_address: str):
        contract = web3.eth.contract(address=contract_address, abi=ERC20_ABI)
        symbol = contract.functions.symbol().call()
        decimal = contract.functions.decimals().call()
        balance_wei = contract.functions.balanceOf(wallet_address).call()
        balance = balance_wei / 10**decimal
        return {"balance_wei": balance_wei, "balance": balance, "symbol": symbol, "decimal": decimal}

    def get_eth_balances_single_chain(self, chain: str):
        addresses = self._load_addresses()
        if addresses is None or chain.lower() not in self.web3_instances:
            print(f"{COLORS['RED']}\nPlease select a valid chain or correct file format\n{COLORS['RESET']}")
            return

        # Initialize a list to collect data for each wallet
        dataset = []

        total_eth_balance = 0
        eth_web3 = self.web3_instances[chain.lower()]

        for i, addr in enumerate(addresses, start=1):
            alias, address = self._parse_address(addr, i)
            eth_balance = self._round_decimals_down(float(self.get_eth_balance(eth_web3, address)), 5)
            total_eth_balance += eth_balance
            total_eth_balance = self._round_decimals_down(float(total_eth_balance), 5)
            row = {"Alias": alias, "Address": address, "ETH": eth_balance}
            dataset.append(row)

        dataset.append({"Alias": " ", "Address": "Total ETH", "ETH": total_eth_balance})

        # Print collected data
        headers = dataset[0].keys()
        rows = [x.values() for x in dataset]
        print(f">>> Chain: {chain.capitalize()}")
        print(tabulate.tabulate(rows, headers=headers, tablefmt="psql", showindex=False, numalign="right"))

        # Save data to .xlsx file
        df = pd.DataFrame(dataset)
        filename = f"{chain}_eth_balance.xlsx"
        df.to_excel(filename, index=False, engine="openpyxl")

        print(f"Data has been successfully saved to {filename}")

    def get_eth_balances_all_chains(self):
        addresses = self._load_addresses()
        if addresses is None:
            print(f"{COLORS['RED']}Invalid file format. Please provide either .txt or .json file.{COLORS['RESET']}")
            return

        # Initialize a list to collect data for each wallet
        dataset = []

        for i, addr in enumerate(addresses, start=1):
            alias, address = self._parse_address(addr, i)
            row = {"Alias": alias, "Address": f"{address[:5]}...{address[-5:]}"}

            wallet_balance = 0
            for chain, eth_web3 in self.web3_instances.items():
                eth_balance = self._round_decimals_down(float(self.get_eth_balance(eth_web3, address)), 5)
                wallet_balance += eth_balance
                row[f"{chain}\nETH"] = eth_balance

            row[f"Total\nETH"] = wallet_balance
            dataset.append(row)

        # Print collected data
        headers = dataset[0].keys()
        rows = [x.values() for x in dataset]
        print(tabulate.tabulate(rows, headers=headers, tablefmt="psql", showindex=False, numalign="right"))

        # Save data to .xlsx file
        df = pd.DataFrame(dataset)
        filename = f"multichain_eth_balance.xlsx"
        df.to_excel(filename, index=False, engine="openpyxl")

        print(f"Data has been successfully saved to {filename}")

    def get_token_balances_all_chains(self):
        addresses = self._load_addresses()
        if addresses is None:
            print("Invalid file format. Please provide either a .txt or .json file.")
            return

        # Initialize a list to collect data for each wallet
        results = []

        # Process balances for each address
        for addr in addresses:
            print(f"\n\n>>> ADDRESS: {addr['address']}")
            row = {"Address": addr["address"]}
            total_eth = Decimal("0.0")

            for chain, eth_web3 in self.web3_instances.items():
                print(f"\t>>> CHAIN: {chain}")
                # Retrieve and store ETH balance
                eth_balance = Decimal(self.get_eth_balance(eth_web3, addr["address"]))
                row[f"{chain} ETH"] = eth_balance
                total_eth += eth_balance

                # Retrieve and store token balances for the current chain
                tokens = TOKENS.get(chain, {})
                for token, contract_address in tokens.items():
                    print(f"\t\t>>> TOKEN: {token}")
                    token_info = self.get_token_balance(eth_web3, contract_address, addr["address"])
                    token_balance = Decimal(token_info["balance"] if "balance" in token_info else token_info)
                    row[f"{chain} {token}"] = token_balance

            results.append(row)

        df = pd.DataFrame(results)
        df.to_excel("token_balances.xlsx", index=False, engine="openpyxl")
        print("Data has been successfully saved to 'token_balances.xlsx'")
