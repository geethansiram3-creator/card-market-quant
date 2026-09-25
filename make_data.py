import csv
import random
from datetime import date, timedelta
#estimated starting prices pulled off of Collector and Tcgplayer
cards = [
    ("Charizard ex", 120),
    ("Umbreon VMAX", 900),
    ("Pikachu", 45),
    ("Mewtwo ex", 30),
    ("Rayquaza VMAX", 350),
    ("Sylveon ex", 80),
    ("Gengar", 25),
    ("Snorlax", 60),
]

today = date.today()
current = {}

with open("sales.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["card", "date", "price"])
    for name, price in cards:
        for days_ago in range(90, -1, -1):
            price *= random.uniform(0.97, 1.032)
            if random.random() < 0.6:
                sale = price * random.uniform(0.9, 1.1)
                if random.random() < 0.03:
                    sale *= random.choice([0.2, 4])
                writer.writerow([name, today - timedelta(days=days_ago), round(sale, 2)])
        current[name] = price

with open("listings.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["card", "price"])
    for name, price in current.items():
        writer.writerow([name, round(price * random.uniform(0.7, 1.3), 2)])

print("Made sales.csv and listings.csv")
