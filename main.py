import tkinter as tk
from tkinter import ttk, messagebox
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

        tk.Label(add_window, text="Ingredient Name:").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Current Amount:").grid(row=1, column=0, padx=10, pady=5)
        current_amount_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Target Amount:").grid(row=2, column=0, padx=10, pady=5)
        target_amount_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Prepped By:").grid(row=3, column=0, padx=10, pady=5)
        prepped_by_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Waste Amount:").grid(row=4, column=0, padx=10, pady=5)
        waste_amount_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        def submit():
            try:
                name = name_entry.get()
                current_amount = int(current_amount_entry.get())
                target_amount = int(target_amount_entry.get())
                prepped_by = prepped_by_entry.get()
                waste_amount = int(waste_amount_entry.get())

                if not name or not prepped_by:
                    raise ValueError("Name and Prepped By fields cannot be empty.")

                ingredient = Ingredient(name, current_amount, target_amount, prepped_by, waste_amount)
                self.inventory.add_ingredient(ingredient)
                messagebox.showinfor("Success", "Ingredient added successfully!")
                add_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        tk.Button(add_window, text="Submit", command=submit).grid(row=5, column=0, columnspan=2, pady=10)

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
                ingredient.current_amount,
                ingredient.target_amount,
                ingredient.prepped_by,
                ingredient.waste_amount,
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