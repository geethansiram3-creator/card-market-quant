# Card Market Quant

I work as a trading card analyst and price Pokemon cards every week. I built this to make that faster and more accurate.

It takes card sales and figures out what each card is actually worth. It throws out weird sales like typos and counts recent sales more than old ones. From there it finds underpriced listings, shows which way the market is moving, and tells you if a card is worth grading.

## How to run it

python make_data.py
python cards.py

make_data.py creates sample data. To use real sales, put them in sales.csv and your listings in listings.csv.
