def analyze_purchases(purchases: list) -> dict:
    customer_counts = {}
    category_counts = {}
    all_customers = set()

    for cust, cat, prod in purchases:
        all_customers.add(cust)
        if cust not in customer_counts:
            customer_counts[cust] = {}
        if cat not in customer_counts[cust]:
            customer_counts[cust][cat] = {}
        customer_counts[cust][cat][prod] = customer_counts[cust][cat].get(prod, 0) + 1
        if cat not in category_counts:
            category_counts[cat] = {}
        category_counts[cat][prod] = category_counts[cat].get(prod, 0) + 1

    result = {}
    for cust in sorted(all_customers):
        result[cust] = {}
        if cust in customer_counts:
            for cat, prods in customer_counts[cust].items():
                duplicate_sum = 0
                for count in prods.values():
                    if count > 1:
                        duplicate_sum += count
                if duplicate_sum > 0:
                    result[cust][cat] = duplicate_sum

    result["most_frequent"] = {}
    for cat, prods in category_counts.items():
        best_product = ""
        max_count = 0
        for prod in sorted(prods.keys()):
            count = prods[prod]
            if count > max_count:
                max_count = count
                best_product = prod
        result["most_frequent"][cat] = best_product
    return result

purchases = [
    ("cust1", "electronics", "laptop"),
    ("cust2", "groceries", "apple"),
    ("cust1", "electronics", "laptop"),
    ("cust1", "electronics", "mouse"),
    ("cust2", "groceries", "apple"),
    ("cust2", "groceries", "banana"),
    ("cust3", "groceries", "banana"),
    ("cust3", "groceries", "apple"),
    ("cust3", "electronics", "camera"),
]

import pprint
pprint.pprint(analyze_purchases(purchases), sort_dicts=False)