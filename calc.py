import os
import yaml
import pathlib
import pandas as pd


RECIPE_FILE = "recipes.yaml"

ROOT_DIR = str(pathlib.Path(__file__).parent.resolve())
FULL_RECIPE_FILE_PATH = os.path.join(ROOT_DIR, RECIPE_FILE)
pd.set_option('display.max_rows', None)


def read_recipes(filepath: str):
    with open(filepath, "r", encoding="utf8") as data:
        try:
            return yaml.safe_load(data)
        except yaml.YAMLError as exc:
            print(exc)


def add_to_recipe(recipe: dict, name_item: str, number_item: int):
    if not name_item in recipe:
        recipe[name_item] = 0
    recipe[name_item] += number_item


def get_recipe(recipes: dict, full_recipe: dict, name_item: str, number_item: int, print_indent=0):
    print(f"{'  ' * print_indent} - {number_item}x {name_item}")
    recipe_item = recipes.get(name_item)
    if not recipe_item:
        return name_item, number_item
    
    for item, number in recipe_item.items():
        recipe = get_recipe(recipes, full_recipe, item, number * number_item, print_indent + 1)
        if recipe:
            add_to_recipe(full_recipe, recipe[0], recipe[1])
        

def get_full_recipe(recipes: dict, name_item: str, number_item: int):
    print(f"\nCalculating primitives needed to craft {number_item}x {name_item}...")
    full_recipe = {}
    get_recipe(recipes, full_recipe, name_item, number_item)
    return full_recipe


def print_full_recipe(full_recipe: dict, desired_item: str, desired_quantity: str):
    df = pd.DataFrame(full_recipe.items(), columns=['Item', 'Quantity'])
    sorted_df = df.sort_values(by='Quantity', ascending=False)
    print(f"\nPrimitives needed to craft {desired_quantity}x {desired_item}:")
    print("-" * 40)
    print(sorted_df.to_string(index=False))


def main():
    recipes: dict = read_recipes(FULL_RECIPE_FILE_PATH)

    while True:
        desired_item = input(" (?) Desired item name: ")
        if desired_item in recipes:
            break
        print("     [!] ERROR: Unknown item name! Please try again...")

    while True:
        try:
            user_input = input(" (?) Desired item quantity [1]: ")
            desired_quantity = int(user_input) if user_input else 1
            if desired_quantity > 0:
                break
            else:
                print("     [!] ERROR: Please enter a number greater than 0.")
        except ValueError:
            print("     [!] ERROR: Please enter a valid number.")

    full_recipe = get_full_recipe(recipes, desired_item, desired_quantity)
    print_full_recipe(full_recipe, desired_item, desired_quantity)
    

if __name__ == "__main__":
    main()