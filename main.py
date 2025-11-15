from collections import Counter

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

min_support = 0.6
min_confidence = 0.8


def gen_itemsets(vertical, freq, min_support_count):
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

            # Apriori principle
            if len(curr_items) == len(next_items) and curr_items[:-1] == next_items[:-1]:
                new_items = curr_items + [next_items[-1]]
                new_item = ','.join(sorted(new_items))

                #intersection
                new_tids = curr_tids.intersection(next_tids)

                if len(new_tids) >= min_support_count:
                    freq[new_item] = new_tids
                    new_vertical[new_item] = new_tids

    return gen_itemsets(new_vertical, freq, min_support_count)

def generate_association_rules(freq):
    rules = []
    for itemset, tids in freq.items():
        items = itemset.split(',')
        if len(items) < 2:
            continue

        for i in range(1,len(items)):
            for left in combinations(items, i):
                left = set(left)
                right = set(items) - left
                rules.append((left, right, tids))
    return rules

def extract_strong_rules(all_rules, freq, min_conf):
    strong_rules = []

    for left, right, tids in all_rules:
        left_key = ','.join(sorted(left))

        conf = len(tids) / len(freq[left_key])

        if conf >= min_conf:
            strong_rules.append((left, right, len(tids), conf))

    return strong_rules


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

min_support_count = int(min_support * len(df))

#Build vertical format
for index, row in df.iterrows():
    tid = row['TiD']
    # Split the string by commas and strip spaces
    items = [x.strip() for x in str(row['items']).split(',')]
    for item in items:
        if item not in vertical:
            vertical[item] = set()
        vertical[item].add(tid)

for item, tids in vertical.items():
    print(f"{item}: {tids}")

print("========================================")

# Generate the first frequent itemset
L1 = {}
for item, tids in vertical.items():
    if len(tids) >= min_support_count:
        L1[item] = tids

print("Data in Vertical format")
for item,tids in L1.items():
    print(f"{item}: {tids}")

print("===============================================================================")
freq = L1.copy()
new_freq = gen_itemsets(L1, freq, min_support_count)

print("All Frequent Itemsets:")
for item,tids in new_freq.items():
    print(f"{item}: {tids}")

print("==============================================================================")
print("Print All Association Rules")
association_rules = generate_association_rules(new_freq)
for rule in association_rules:
    print(rule)

print("==============================================================================")
print("Print Strong Rules")
strong_rules = extract_strong_rules(association_rules, new_freq, min_confidence)
for strong_rule in strong_rules:
    print(strong_rule)

print("==============================================================================")
print("Print Strong Rules with Lift values")
lift_values = calculate_lift(strong_rules, new_freq, len(df))
for lift_value in lift_values:
    print(lift_value)


#Visualization

rule_df = pd.DataFrame(lift_values, columns=['Left','Right','Conf','Lift'])

# Lift Histogram
plt.figure(figsize=(8,6))
plt.hist(rule_df['Lift'], bins=5, edgecolor='black')
plt.xlabel('Lift')
plt.ylabel('Frequency')
plt.title('Lift Value Distribution for Strong Rules')
plt.grid(axis='y', alpha=0.3)
plt.show()

# Frequent Itemsets per Level
plt.figure(figsize=(8,6))
levels = [len(item.split(',')) for item in new_freq.keys()]
level_counts = Counter(levels)

bars = plt.bar(level_counts.keys(), level_counts.values())
plt.xlabel('Itemset Size (k)')
plt.ylabel('Count of Frequent Itemsets')
plt.title('Frequent Itemsets per Level (L1, L2, L3...)')
plt.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.annotate(str(height),
                 xy=(bar.get_x() + bar.get_width()/2, height),
                 xytext=(0,5),
                 textcoords='offset points',
                 ha='center', fontsize=10)

plt.show()
