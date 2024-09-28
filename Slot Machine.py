#Its Slot Machine Game
#Disclaimer:  Not supporting Betting Its just for practice


import random

MAX_LINES = 3
MIN_BET = 1
MAX_BET = 100

ROWS = 3
COLS = 3

symbol_value = {"A": 5, "B": 4, "C": 3, "D": 2}
symbol_count = {"A": 2, "B": 4, "C": 6, "D": 8}


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns


def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(f"{column[row]} | ", end="")
            else:
                print(f"{column[row]}", end="")
        print("\n")


def get_winnings(lines, columns, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if symbol != column[line]:
                break
        else:
            winnings += bet * values[symbol]
            winning_lines.append(line + 1)
    return winnings, winning_lines


def deposit():
    while True:
        amount = input("Enter the amount to deposit: $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            print("\nAmount should be greater than 0\n")
        else:
            print("\nInvalid amount. Please enter a valid number\n")
    return amount


def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1 - {MAX_LINES})? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            print(f"Lines should be greater than 0 and less than {MAX_LINES}\n")
        else:
            print("\nInvalid lines. Please enter a valid number\n")
    return lines


def get_bet():
    while True:
        bet = input(
            f"Enter the number of amount to bet on each line ({MIN_BET} - {MAX_BET})? "
        )
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            print(f"Bet should be greater than 0 and less than {MAX_BET}\n")
        else:
            print("\nInvalid beting amount. Please enter a valid number\n")
    return bet


def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(
                f"\nYou don't have enough balance to place a bet of ${total_bet}. Your balance is ${balance}"
            )
        else:
            break
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print("\nSpinning the wheel...\n")
    print_slot_machine(slots)
    winnings, winning_lines = get_winnings(lines, slots, bet, symbol_value)
    print(f"\nYou won ${winnings}\n")
    print(f"\nYou won on lines: ", *winning_lines)
    print("")
    return winnings - total_bet


balance = deposit()
while True:
    print(f"\nCurrent balance is ${balance}\n")
    if balance == 0:
        print("You have run out of money, game over")
        break
    action = input("Do you want to play or quit(p/q)? ").lower()
    if action == "p":
        balance += spin(balance)
    elif action == "q":
        print(f"\nThanks for playing. Your final balance is ${balance}")
        break
    print(f"You left with ${balance}")

