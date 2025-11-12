import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns

def gen_itemsets(vertical, freq, min_sup):
    if len(vertical) <= 1:
        return freq

    new_vertical = {}
    new_tids = []

    vertical_items = list(vertical.keys())
    vertical_tids = list(vertical.values())

    for i in range(len(vertical) - 1):
        for j in range(i + 1, len(vertical) - 1):
            curr_item = vertical_items[i]
            next_item = vertical_items[j]
            curr_tids = vertical_tids[i]
            next_tids = vertical_tids[j]

            if curr_item[1:] == next_item[:-1]:
                new_item = curr_item[0] + next_item
                new_tids = curr_tids.intersection(next_tids)

            if len(new_tids) >= min_sup:
                freq[new_item] = new_tids
                new_vertical[new_item] = new_tids

    return gen_itemsets(new_vertical, freq, min_sup)

df = pd.read_excel("Horizontal_Format.xlsx")
vertical = {}

# Step 3: Build vertical format
for column, row in df.iterrows():
    tid = row['TiD']
    # Split the string by commas and strip spaces
    items = [x.strip() for x in str(row['items']).split(',')]
    for item in items:
        if item not in vertical:
            vertical[item] = set()
        vertical[item].add(tid)

# Step 4: Display the vertical representation
for item, tids in vertical.items():
    print(f"{item}: {tids}")

print("========================================")

min_support = 2

l1 = {}
for item, tids in vertical.items():
    if len(tids) >= min_support:
        l1[item] = tids

for item,tids in l1.items():
    print(f"{item}: {tids}")

print("========================================")
freq = {}
new_freq = gen_itemsets(l1,freq,2)


for item,tids in new_freq.items():
    print(f"{item}: {tids}")