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
        self.current_frame = None
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
        self.root.geometry("600x400")

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.show_main_menu()

    def show_main_menu(self):
        """Display the main menu."""
        self.clear_frame()
        self.current_frame = "main_menu"

        tk.Button(self.container, text="Add Ingredient", command=self.show_category_selection).pack(pady=10)
        tk.Button(self.container, text="View Inventory", command=self.show_view_inventory).pack(pady=10)
        tk.Button(self.container, text="Generate Report", command=self.generate_report).pack(pady=10)

    def show_category_selection(self):
        """Display the category selection screen."""
        self.clear_frame()
        self.current_frame = "category_selection"

        tk.Label(self.container, text="Select Ingredient Category:").pack(pady=10)

        for category in self.categories.keys():
            tk.Button(self.container, text=category, command=lambda cat=category: self.show_ingredient_selection(cat)).pack(pady=5)

        self.add_back_button()

    def show_ingredient_selection(self, category):
        """Display the ingredient selection screen for a given category."""
        self.clear_frame()
        self.current_frame = "ingredient_selection"

        tk.Label(self.container, text=f"Select {category} Ingredient:").pack(pady=10)

        for ingredient, target_amount in self.categories[category].items():
            tk.Button(self.container, text=ingredient, command=lambda ing=ingredient, target=target_amount: self.open_add_ingredient(ing, target)).pack(pady=5)

        self.add_back_button()

    def open_add_ingredient(self, ingredient_name, target_amount):
        """Display the add ingredient screen."""
        self.clear_frame()
        self.current_frame = "add_ingredient"

        tk.Label(self.container, text=f"Ingredient: {ingredient_name}").pack(pady=5)
        tk.Label(self.container, text=f"Target Amount: {target_amount} pans").pack(pady=5)

        tk.Label(self.container, text="Current Amount (in pans):").pack(pady=5)
        self.current_amount_entry = tk.Entry(self.container)
        self.current_amount_entry.pack(pady=5)

        tk.Label(self.container, text=f"Prepped By: {self.user_name}").pack(pady=5)

        tk.Label(self.container, text="Waste Amount (in pans):").pack(pady=5)
        self.waste_amount_entry = tk.Entry(self.container)
        self.waste_amount_entry.pack(pady=5)

        tk.Button(self.container,text="Submit", command=lambda: self.submit_ingredient(ingredient_name, target_amount)).pack(pady=10)

        self.add_back_button()

    def submit_ingredient(self, ingredient_name, target_amount):
        """Handle the submission of a new ingredient."""
        try:
            current_amount = int(self.current_amount_entry.get())
            waste_amount = int(self.waste_amount_entry.get())

            ingredient = Ingredient(ingredient_name, current_amount, target_amount, self.user_name, waste_amount)
            self.inventory.add_ingredient(ingredient)
            messagebox.showinfo("Success", f"{ingredient_name} added/updated successfully!")
            self.show_main_menu()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def show_view_inventory(self):
        """Display the inventory view."""
        self.clear_frame()
        self.current_frame = "view_inventory"

        columns = ("Name", "Current Amount", "Target Amount", "Prepped By", "Waste Amount", "Prep Time")
        tree = ttk.Treeview(self.container, columns=columns, show="headings")
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

        self.add_back_button()

    def generate_report(self):
        """Display the inventory report."""
        self.clear_frame()
        self.current_frame = "generate_report"

        report = self.inventory.generate_report()
        tk.Label(self.container, text="Inventory Report", font=("Arial", 16)).pack(pady=10)
        text_widget = tk.Text(self.container)
        text_widget.insert(tk.END, report)
        text_widget.pack(pady=10)

        self.add_back_button()

    def add_back_button(self):
        """Add a Back button to the current frame."""
        tk.Button(self.container, text="Back", command=self.show_main_menu).pack(pady=10)

    def clear_frame(self):
        """Clear all widgets from the current frame."""
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()