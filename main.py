import curses
from config import RPC_NODES
from src.balances import ETHBalances


def display_menu(stdscr, title, options):
    stdscr.clear()

    current_option = 0

    stdscr.addstr(f"\n{title}:\n\n")
    for idx, option in enumerate(options):
        if idx == current_option:
            stdscr.addstr(f"{idx + 1}. {option}\n", curses.A_REVERSE)
        else:
            stdscr.addstr(f"{idx + 1}. {option}\n")

    stdscr.addstr("\nUse arrow keys to navigate, press Enter to select.")

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP:
            current_option = (current_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            break

        stdscr.clear()
        stdscr.addstr(f"{title}:\n\n")
        for idx, option in enumerate(options):
            if idx == current_option:
                stdscr.addstr(f"{idx + 1}. {option}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"{idx + 1}. {option}\n")

        stdscr.addstr("\nUse arrow keys to navigate, press Enter to select.")

    return current_option


if __name__ == "__main__":
    eth_balances = ETHBalances()
    options = [
        "Retrieve ETH Balance | Single Chain",
        "Retrieve ETH Balance | All Chains",
        "Retrieve Preset Token Balances | Single Chain",
    ]
    user_option = curses.wrapper(display_menu, "Please select an option", options)
    print(f"You selected option {user_option + 1}\n")

    if user_option == 0:
        chain_options = list(RPC_NODES.keys())
        chain_option = curses.wrapper(display_menu, "Please select a chain", chain_options)
        chain = chain_options[chain_option]
        eth_balances.get_eth_balances_single_chain(chain)
        print("\n")

    elif user_option == 1:
        eth_balances.get_eth_balances_all_chains()
        print("\n")

    elif user_option == 2:
        chain_options = list(RPC_NODES.keys())
        chain_option = curses.wrapper(display_menu, "Please select a chain", chain_options)
        chain = chain_options[chain_option]
        eth_balances.get_tokens_balances_single_chain(chain)
        print("\n")
