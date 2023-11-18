import json
import random
def get_one_restaurant():
    with open('restaurants.json', 'r', encoding='utf8') as f:
        restaurant = json.load(f)
    return random.choice(restaurant)

def get_all_restaurant():
    with open('restaurants.json', 'r', encoding='utf8') as f:
        restaurant = json.load(f)
    quantity = len(restaurant)
    return restaurant, quantity