import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
from itertools import combinations

from fontTools.misc.cython import returns

min_support = 2
min_confidence = 0.6


def gen_itemsets(vertical, freq, min_sup):
    if len(vertical) <= 1:
        return freq

    new_vertical = {}
    vertical_items = list(vertical.keys())

    for i in range(len(vertical_items)):
        for j in range(i + 1, len(vertical_items)):
            curr_item = vertical_items[i]
            next_item = vertical_items[j]
            curr_tids = vertical[curr_item]
            next_tids = vertical[next_item]


            curr_items = curr_item.split(',')
            next_items = next_item.split(',')

            # Check if they share first k-1 items (Apriori principle)
            if len(curr_items) == len(next_items) and curr_items[:-1] == next_items[:-1]:
                new_items = curr_items + [next_items[-1]]
                new_item = ','.join(sorted(new_items))

                #intersection of TIDs
                new_tids = curr_tids.intersection(next_tids)

                if len(new_tids) >= min_sup:
                    freq[new_item] = new_tids
                    new_vertical[new_item] = new_tids

    return gen_itemsets(new_vertical, freq, min_sup)

def generate_rules(freq, min_conf):
    rules = []
    for itemset, tids in freq.items():
        items = itemset.split(',')
        if len(items) < 2:
            continue

        for i in range(1,len(items)):
            for left in combinations(items, i):
                left = set(left)
                right = set(items) - left
                left_key = ','.join(sorted(left))

                if left_key in freq:
                    conf = len(tids) / len(freq[left_key])
                    if conf >= min_conf:
                        rules.append((left,right,len(tids),conf))
    return rules

def calculate_lift(rules, freq ,total_transactions):
    lift_values = []
    for left , right , support_count, conf in rules:
       left_key = ','.join(sorted(left))
       right_key = ','.join(sorted(right))

       support_left = len(freq[left_key]) / total_transactions
       support_right = len(freq[right_key]) / total_transactions
       support_union = support_count / total_transactions

       lift = support_union / (support_left * support_right)
       lift_values.append((left,right,conf,lift))

    return lift_values


df = pd.read_excel("Horizontal_Format.xlsx")
vertical = {}

# Step 3: Build vertical format
for index, row in df.iterrows():
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


L1 = {}
for item, tids in vertical.items():
    if len(tids) >= min_support:
        L1[item] = tids

for item,tids in L1.items():
    print(f"{item}: {tids}")

print("===============================================================================")
freq = L1.copy()
new_freq = gen_itemsets(L1, freq, min_support)

print("All Frequent Itemsets:")
for item,tids in new_freq.items():
    print(f"{item}: {tids}")

print("==============================================================================")
print("Print Strong rules")
strong_rules = generate_rules(freq, min_confidence)
for rule in strong_rules:
    print(rule)


print("===============================================================================")
print("Print Strong rules with Lift values")
lift_values = calculate_lift(strong_rules, freq, len(df))
for lift_value in lift_values:
    print(lift_value)

