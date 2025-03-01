import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
        existing_ingredient = self.get_ingredient(ingredient.name)
        if existing_ingredient:
            existing_ingredient.update_amount(ingredient.current_amount)
            existing_ingredient.prepped_by = ingredient.prepped_by
            existing_ingredient.prep_time = ingredient.prep_time
        else:
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

#    def view_inventory(self):
#        for ingredient in self.ingredients:
#            print(f"{ingredient.name}: {ingredient.current_amount}/{ingredient.target_amount}")

class UserInterface:
    def __init__(self, root):
        self.root = root
        self.inventory = Inventory()
        self.user_name = self.get_user_name()
        self.setup_ui()

        self.categories = {
            "Meats": {
                "Ham": 4,
                "Turkey": 4,
                "Chicken": 2,
                "Steak": 5
            },
            "Vegetables": {
                "Lettuce": 2,
                "Tomatoes": 2,
                "Onions": 4,
                "Pickles": 2
            }
        }

    def get_user_name(self):
        user_name = simpledialog.askstring("Input", "Enter your name:", parent=self.root)
        if not user_name:
            messagebox.showerror("Error", "Name is required to use the application.")
            self.root.destroy()
        return user_name

    def setup_ui(self):
        self.root.title("Subway Prepped Inventory Manager")

        tk.Button(self.root, text="Add Ingredient", command=self.open_category_selection_window).pack(pady=10)
        tk.Button(self.root, text="View Inventory", command=self.open_view_inventory_window).pack(pady=10)
        tk.Button(self.root, text="Generate Report", command=self.generate_report).pack(pady=10)

    def open_category_selection_window(self):
        category_window = tk.Toplevel(self.root)
        category_window.title("Select Ingredient Category")

        tk.Label(category_window, text="Select Ingredient Category:").pack(pady=10)

        for category in self.categories.keys():
            tk.Button(category_window, text=category, command=lambda cat=category: self.open_ingredient_selection_window(cat)).pack(pady=5)

    def open_ingredient_selection_window(self, category):
        ingredient_window = tk.Toplevel(self.root)
        ingredient_window.title(f"Select {category} Ingredient")

        tk.Label(ingredient_window, text=f"Select {category} Ingredient:").pack(pady=10)

        for ingredient, target_amount in self.categories[category].items():
            tk.Button(ingredient_window, text=ingredient, command=lambda ing=ingredient, target=target_amount: self.open_add_ingredient_window(ing, target)).pack(pady=5)

    def open_add_ingredient_window(self, ingredient_name, target_amount):
        add_window = tk.Toplevel(self.root)
        add_window.title(f"Add {ingredient_name}")

        tk.Label(add_window, text=f"Ingredient: {ingredient_name}").pack(pady=5)
        tk.Label(add_window, text=f"Target Amount: {target_amount} pans").pack(pady=5)

        tk.Label(add_window, text="Current Amount (in pans):").pack(pady=5)
        current_amount_entry = tk.Entry(add_window)
        current_amount_entry.pack(pady=5)

        tk.Label(add_window, text=f"Prepped By: {self.user_name}").pack(pady=5)

        tk.Label(add_window, text="Waste Amount (in pans):").pack(pady=5)
        waste_amount_entry = tk.Entry(add_window)
        waste_amount_entry.pack(pady=5)

        def submit():
            try:
                current_amount = int(current_amount_entry.get())
                waste_amount = int(waste_amount_entry.get())

                ingredient = Ingredient(ingredient_name, current_amount, target_amount, self.user_name, waste_amount)
                self.inventory.add_ingredient(ingredient)
                messagebox.showinfo("Success", f"{ingredient_name} added/updated successfully!")
                add_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        tk.Button(add_window, text="Submit", command=submit).pack(pady=10)

    def open_view_inventory_window(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Inventory")

        columns = ("Name", "Current Amount", "Target Amount", "Prepped By", "Waste Amount", "Prep Time")
        tree = ttk.Treeview(view_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(padx=10,pady=10)

        for ingredient in self.inventory.ingredients:
            tree.insert("", "end", values=(
                ingredient.name,
                f"{ingredient.current_amount} pans",
                f"{ingredient.target_amount} pans",
                ingredient.prepped_by,
                f"{ingredient.waste_amount} pans",
                ingredient.prep_time.strftime("%Y-%m-%d %H:%M:%S")
            ))

    def generate_report(self):
        report = self.inventory.generate_report()
        report_window = tk.Toplevel(self.root)
        report_window.title("Inventory Report")

        tk.Label(report_window, text="Inventory Report", font=("Arial", 16)).pack(pady=10)
        tk.Text(report_window).insert(tk.END, report)
        tk.Button(report_window, text="Close", command=report_window.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()