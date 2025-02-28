import tkinter as tk
from tkinter import ttk
from datetime import datetime

class Ingredient:
    def __init__(self, name, current_amount, target_amount, prepped_by, waste_amount=0):
        self.name = name
        self.current_amount = current_amount
        self.target_amount = target_amount
        self.prepped_by = prepped_by
        self.prep_time = datetime.now()
        self.waste_amount = waste_amount

    def update_amount(self, new_amount):
        self.current_amount = new_amount

    def log_waste(self, waste_amount):
        self.waste_amount += waste_amount

class Inventory:
    def __init__(self):
        self.ingredients = []

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def view_inventory(self):
        for ingredient in self.ingredients:
            print(f"{ingredient.name}: {ingredient.current_amount}/{ingredient.target_amount}")

class UserInterface:
    def __init__(self, root):
        self.root = root
        self.inventory = Inventory()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Subway Prepped Inventory Manager")
        tk.Button(self.root, text="Add Ingredient", command=self.add_ingredient).pack()

    def add_ingredient(self):
        pass
    def view_inventory(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()