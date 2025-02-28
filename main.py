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

    def __str__(self):
        return(f"{self.name}: Current{self.current_amount}, Target={self.target_amount},"
               f"Prepped By={self.prepped_by}, Waste={self.waste_amount}, Prep Time={self.prep_time}")

class Inventory:
    def __init__(self):
        self.ingredients = []

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def remove_ingredient(self, ingredient_name):
        self.ingredients = [ing for ing in self.ingredients if ing.name != ingredient_name]

    def get_ingredient(self, ingredient_name):
        for ingredient in self.ingredients:
            if ingredient.name == ingredient_name:
                return ingredient
        return None

    def generate_report(self):
        report = []
        for ingredient in self.ingredients:
            report.append(str(ingredient))
        return "\n".join(report)

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

        tk.Button(self.root, text="Add Ingredient", command=self.open_add_ingredient_window).pack(pady=10)
        tk.Button(self.root, text="View Inventory", command=self.open_view_inventory_window).pack(pady=10)
        tk.Button(self.root, text="Generate Report", command=self.generate_report).pack(pady=10)

    def open_add_ingredient_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Ingredient")

    def open_view_inventory_window(self):
        pass

    def generate_report(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()