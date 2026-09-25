#transfer everything over from mac file
import csv
from datetime import date
from statistics import median
#estimated random numbers from the internet
FEES = 0.12
SHIPPING = 1.00
TARGET_MARGIN = 0.25
HALF_LIFE = 14


def load_sales():
    sales = {}
    with open("sales.csv") as f:
        for row in csv.DictReader(f):
            day = date.fromisoformat(row["date"])
            sales.setdefault(row["card"], []).append((day, float(row["price"])))
    return sales


def fair_value(history):
    prices = [price for _, price in history]
    mid = median(prices)
    spread = max(median(abs(p - mid) for p in prices), mid * 0.01)
    last = max(day for day, _ in history)
    total = 0
    weights = 0
    for day, price in history:
        if abs(price - mid) / spread > 5:
            continue
        weight = 0.5 ** ((last - day).days / HALF_LIFE)
        total += weight * price
        weights += weight
    return total / weights


def change(history, days=30):
    last = max(day for day, _ in history)
    old = [(day, price) for day, price in history if (last - day).days >= days]
    if len(old) < 3:
        return None
    return fair_value(history) / fair_value(old) - 1


def after_fees(value):
    return value * (1 - FEES) - SHIPPING


def max_buy(value):
    return after_fees(value) / (1 + TARGET_MARGIN)


def ask_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Enter a number.")


def show_prices(sales):
    print(f"\n{'Card':<16}{'Fair value':>12}{'Max buy':>10}{'30 day':>9}")
    for card, history in sorted(sales.items()):
        value = fair_value(history)
        move = change(history)
        move_text = f"{move:+.1%}" if move is not None else "n/a"
        print(f"{card:<16}{value:>12.2f}{max_buy(value):>10.2f}{move_text:>9}")


def show_deals(sales):
    rows = []
    with open("listings.csv") as f:
        for row in csv.DictReader(f):
            if row["card"] not in sales:
                continue
            ask = float(row["price"])
            value = fair_value(sales[row["card"]])
            edge = (after_fees(value) - ask) / ask
            rows.append((edge, row["card"], ask, value))

    print(f"\n{'Card':<16}{'Ask':>10}{'Fair value':>12}{'Edge':>9}  Call")
    for edge, card, ask, value in sorted(rows, reverse=True):
        call = "BUY" if edge > 0.15 else "PASS" if edge < 0 else "OK"
        print(f"{card:<16}{ask:>10.2f}{value:>12.2f}{edge:>+9.1%}  {call}")


def show_market(sales):
    moves = [change(h) for h in sales.values()]
    moves = [m for m in moves if m is not None]
    if not moves:
        print("\nNot enough history yet.")
        return
    up = sum(1 for m in moves if m > 0)
    print(f"\nAverage 30 day move: {sum(moves) / len(moves):+.1%}")
    print(f"Cards up: {up}   Cards down: {len(moves) - up}")


def grading():
    cost = ask_number("\nRaw card cost: ")
    fee = ask_number("Grading fee plus shipping: ")
    price10 = ask_number("PSA 10 sells for: ")
    price9 = ask_number("PSA 9 sells for: ")
    price8 = ask_number("PSA 8 sells for: ")
    chance10 = ask_number("Chance of PSA 10 (%): ") / 100
    chance9 = ask_number("Chance of PSA 9 (%): ") / 100
    if chance10 + chance9 > 1:
        print("Chances add up to more than 100%.")
        return
    chance8 = 1 - chance10 - chance9
    expected = (chance10 * price10 + chance9 * price9 + chance8 * price8) * (1 - FEES)
    profit = expected - cost - fee
    print(f"\nExpected sale after fees: {expected:.2f}")
    print(f"Expected profit: {profit:+.2f}")
    print("Grade it" if profit > 0 else "Sell raw")


def main():
    sales = load_sales()
    while True:
        print("\n1. Card prices\n2. Deals\n3. Market trend\n4. Grading calculator\n5. Quit")
        choice = input("Pick one: ").strip()
        if choice == "1":
            show_prices(sales)
        elif choice == "2":
            show_deals(sales)
        elif choice == "3":
            show_market(sales)
        elif choice == "4":
            grading()
        elif choice == "5":
            break


main()
