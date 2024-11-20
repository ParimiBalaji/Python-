import \
    pandas as pd
import tkinter as tk
from tkinter import messagebox

# File paths for inventory and sales data
inventory_file = 'inventory.csv'
sales_file = 'sales.csv'

# Load inventory data
try:
    inventory_df = pd.read_csv(inventory_file, index_col=0)
except FileNotFoundError:
    inventory_df = pd.DataFrame(columns=['Name', 'Price', 'Quantity'])

# Load sales data
try:
    sales_df = pd.read_csv(sales_file, index_col=0)
except FileNotFoundError:
    sales_df = pd.DataFrame(columns=['Name', 'Price', 'Quantity', 'Total'])

# Functions for application functionality
def add_product():
    name = name_entry.get().strip()
    try:
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
    except ValueError:
        messagebox.showerror('Error', 'Please enter valid price and quantity values.')
        return

    if name in inventory_df.index:
        messagebox.showerror('Error', f"Product '{name}' already exists in inventory.")
        return

    inventory_df.loc[name] = [price, quantity]
    messagebox.showinfo('Success', f"Product '{name}' added to inventory.")

def update_product():
    name = name_entry.get().strip()
    if name not in inventory_df.index:
        messagebox.showerror('Error', f"Product '{name}' does not exist in inventory.")
        return

    try:
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
    except ValueError:
        messagebox.showerror('Error', 'Please enter valid price and quantity values.')
        return

    inventory_df.loc[name, 'Price'] = price
    inventory_df.loc[name, 'Quantity'] = quantity
    messagebox.showinfo('Success', f"Product '{name}' updated in inventory.")

def delete_product():
    name = name_entry.get().strip()
    if name not in inventory_df.index:
        messagebox.showerror('Error', f"Product '{name}' does not exist in inventory.")
        return

    inventory_df.drop(name, inplace=True)
    messagebox.showinfo('Success', f"Product '{name}' deleted from inventory.")

def sell_product():
    name = name_entry.get().strip()
    try:
        quantity = int(quantity_entry.get())
    except ValueError:
        messagebox.showerror('Error', 'Please enter a valid quantity.')
        return

    if name not in inventory_df.index:
        messagebox.showerror('Error', f"Product '{name}' does not exist in inventory.")
        return

    if inventory_df.loc[name, 'Quantity'] < quantity:
        messagebox.showerror('Error', f"Not enough quantity of '{name}' available in inventory.")
        return

    inventory_df.loc[name, 'Quantity'] -= quantity
    price = inventory_df.loc[name, 'Price']
    total = price * quantity
    sales_df.loc[len(sales_df)] = [name, price, quantity, total]

    messagebox.showinfo('Success', f"{quantity} units of '{name}' sold.")

def show_inventory():
    inventory_str = inventory_df.to_string()
    messagebox.showinfo('Inventory', inventory_str)

def generate_report():
    report_str = sales_df.to_string()
    messagebox.showinfo('Sales Report', report_str)

def save_inventory():
    inventory_df.to_csv(inventory_file)
    messagebox.showinfo('Success', 'Inventory saved to file.')

def save_sales():
    sales_df.to_csv(sales_file)
    messagebox.showinfo('Success', 'Sales data saved to file.')

# Main application window
root = tk.Tk()
root.title('Grocery Store')
root.configure(bg='white')

# Labels and entry fields
tk.Label(root, text='Product Name:', bg='white').grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text='Price (Rs):', bg='white').grid(row=1, column=0, padx=5, pady=5)
price_entry = tk.Entry(root)
price_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text='Quantity (kgs):', bg='white').grid(row=2, column=0, padx=5, pady=5)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons for functionalities
tk.Button(root, text='Add New Product', highlightbackground='grey', borderwidth=3, command=add_product).grid(row=3, column=0, padx=5, pady=5)
tk.Button(root, text='Update Existing Product', highlightbackground='grey', borderwidth=3, command=update_product).grid(row=3, column=1, padx=5, pady=5)
tk.Button(root, text='Delete Product', highlightbackground='grey', borderwidth=3, command=delete_product).grid(row=4, column=0, padx=5, pady=5)
tk.Button(root, text='Sell Product', highlightbackground='grey', borderwidth=3, command=sell_product).grid(row=4, column=1, padx=5, pady=5)

tk.Button(root, text='Show Inventory', highlightbackground='grey', borderwidth=3, command=show_inventory).grid(row=5, column=0, padx=5, pady=5)
tk.Button(root, text='Show Sales Report', highlightbackground='grey', borderwidth=3, command=generate_report).grid(row=5, column=1, padx=5, pady=5)
tk.Button(root, text='Save Inventory', highlightbackground='grey', borderwidth=3, command=save_inventory).grid(row=6, column=0, padx=5, pady=5)
tk.Button(root, text='Save Sales Data', highlightbackground='grey', borderwidth=3, command=save_sales).grid(row=6, column=1, padx=5, pady=5)

# Run the application
root.mainloop()
