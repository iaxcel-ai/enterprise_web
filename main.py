"""
Scenario: You are building an e-commerce checkout service. Every time a user views their cart,
the system must look up the current price of each item from a master list of N products.
"""

import time
from faker import Faker
from faker_commerce import Provider
import random
import json

fake = Faker()
fake.add_provider(Provider)

def product_generator(n):
    base_id = 100_000

    for i in range(n):
        yield {
            "id": base_id + i,
            "product_name": fake.ecommerce_name() if hasattr(fake, 'ecommerce_name') else fake.catch_phrase(),
            "price": round(random.uniform(5.00, 499.99), 2),
            "category": fake.ecommerce_category() if hasattr(fake, 'ecommerce_category') else fake.bs()
        }

def pretty_print(catalog):
    print(json.dumps(catalog, indent=2))

def linear_search(product_id, products):
    for product in products:
        if product["id"] == product_id:
            return product
    return None

def binary_search(product_id, products):
    low = 0
    high = len(products) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_product = products[mid]
        
        if mid_product["id"] == product_id:
            return mid_product
        elif mid_product["id"] < product_id:
            low = mid + 1
        else:
            high = mid - 1
            
    return None


if __name__ == "__main__":
    N = 1_000
    print(f"Generating {N:,} products...")

    products = list(product_generator(N))

    # print("Sample product:")
    # pretty_print(products[0])

    # Example of searching for a product
    search_id = products[random.randint(0, N-1)]["id"]  # Randomly select an existing product ID
    print("Search Id: ", search_id)
    found_product_linear = linear_search(search_id, products)
    found_product_binary = binary_search(search_id, products)
    print(f"\nSearching for product with ID {search_id}:")
    print("Linear Search Result:")
    pretty_print(found_product_linear)
    print("\nBinary Search Result:")
    pretty_print(found_product_binary)

# def filter_product(product, search_id):
#     return product["id"] == search_id
# 
# def linear_search_filter(product_id, products):
#     prods = filter(lambda p: filter_product(p, product_id), products)
#     return list(prods)[0]
