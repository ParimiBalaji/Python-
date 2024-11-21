import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# File paths for inventory and sales data
inventory_file = 'inventory.csv'
sales_file = 'sales.csv'

# Function to initialize empty files if they don't exist
def initialize_files():
    if not os.path.exists(inventory_file):
        inventory_df = pd.DataFrame(columns=['Name', 'Price', 'Quantity'])
        inventory_df.to_csv(inventory_file, index=False)
        print(f"{inventory_file} created successfully.")

    if not os.path.exists(sales_file):
        sales_df = pd.DataFrame(columns=['Name', 'Price', 'Quantity', 'Total'])
        sales_df.to_csv(sales_file, index=False)
        print(f"{sales_file} created successfully.")

# Call the function to ensure files exist
initialize_files()

# Load inventory data
inventory_df = pd.read_csv(inventory_file, index_col=0)

# Load sales data
sales_df = pd.read_csv(sales_file, index_col=0)

# Functions for application functionality
def add_product():
    set_button_state('disable')
    name = name_entry.get().strip()
    try:
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
    except ValueError:
        messagebox.showerror('Error', 'Please enter valid price and quantity values.')
        set_button_state('normal')
        return

    if name in inventory_df.index:
        messagebox.showerror('Error', f"Product '{name}' already exists in inventory.")
        set_button_state('normal')
        return

    inventory_df.loc[name] = [price, quantity]
    messagebox.showinfo('Success', f"Product '{name}' added to inventory.")
    set_button_state('normal')

def update_product():
    set_button_state('disable')
    name = name_entry.get().strip()
    if name not in inventory_df.index:
        messagebox.showerror('Error', f"Product '{name}' does not exist in inventory.")
        set_button_state('normal')
        return

    try:
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
    except ValueError:
        messagebox.showerror('Error', 'Please enter valid price and quantity values.')
        set_button_state('normal')
        return

    inventory_df.loc[name, 'Price'] = price
    inventory_df.loc[name, 'Quantity'] = quantity
    messagebox.showinfo('Success', f"Product '{name}' updated in inventory.")
    set_button_state('normal')

def delete_product():
    set_button_state('disable')
    name = name_entry.get().strip()
    if name not in inventory_df.index:
        messagebox.showerror('Error', f"Product '{name}' does not exist in inventory.")
        set_button_state('normal')
        return

    inventory_df.drop(name, inplace=True)
    messagebox.showinfo('Success', f"Product '{name}' deleted from inventory.")
    set_button_state('normal')

def sell_product():
    set_button_state('disable')
    name = name_entry.get().strip()
    try:
        quantity = int(quantity_entry.get())
    except ValueError:
        messagebox.showerror('Error', 'Please enter a valid quantity.')
        set_button_state('normal')
        return

    if name not in inventory_df.index:
        messagebox.showerror('Error', f"Product '{name}' does not exist in inventory.")
        set_button_state('normal')
        return

    if inventory_df.loc[name, 'Quantity'] < quantity:
        messagebox.showerror('Error', f"Not enough quantity of '{name}' available in inventory.")
        set_button_state('normal')
        return

    # Update inventory
    inventory_df.loc[name, 'Quantity'] -= quantity
    price = inventory_df.loc[name, 'Price']
    total = price * quantity

    # Create a new DataFrame row to append
    new_row = pd.DataFrame({
        'Name': [name],
        'Price': [price],
        'Quantity': [quantity],
        'Total': [total]
    })

    # Append the new row using pd.concat()
    global sales_df  # Ensure global modification
    sales_df = pd.concat([sales_df, new_row], ignore_index=True)

    messagebox.showinfo('Success', f"{quantity} units of '{name}' sold.")
    set_button_state('normal')

def show_inventory():
    inventory_str = inventory_df.to_string(col_space=20)
    messagebox.showinfo('Inventory', inventory_str)

def generate_report():
    report_str = sales_df.to_string()
    messagebox.showinfo('Sales Report', report_str)

def save_inventory():
    set_button_state('disable')
    inventory_df.to_csv(inventory_file)
    messagebox.showinfo('Success', 'Inventory saved to file.')
    set_button_state('normal')

def save_sales():
    set_button_state('disable')
    sales_df.to_csv(sales_file)
    messagebox.showinfo('Success', 'Sales data saved to file.')
    set_button_state('normal')

def set_button_state(state):
    for button in button_frame.winfo_children():
        button.config(state=state)

# Main application window
root = tk.Tk()
root.title('Grocery Store')
root.geometry('600x500')  # Set the window size
root.configure(bg='#f0f0f0')

# Style for widgets
style = ttk.Style()
style.configure('TButton', font=('Arial', 10, 'bold'), padding=10)
style.configure('TLabel', font=('Arial', 12), background='#f0f0f0')
style.configure('TEntry', font=('Arial', 12), padding=5)
style.configure('TFrame', background='#f0f0f0')

# Frame for input fields and buttons
frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

# Labels and entry fields
ttk.Label(frame, text='Product Name:', anchor='center').grid(row=0, column=0, padx=10, pady=10, sticky='ew')
name_entry = ttk.Entry(frame)
name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

ttk.Label(frame, text='Price (Rs):', anchor='center').grid(row=1, column=0, padx=10, pady=10, sticky='ew')
price_entry = ttk.Entry(frame)
price_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

ttk.Label(frame, text='Quantity (kgs):', anchor='center').grid(row=2, column=0, padx=10, pady=10, sticky='ew')
quantity_entry = ttk.Entry(frame)
quantity_entry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

# Buttons for functionalities
button_frame = ttk.Frame(root, padding=10)
button_frame.grid(row=1, column=0, pady=10, sticky='nsew')

ttk.Button(button_frame, text='Add New Product', command=add_product).grid(row=0, column=0, padx=10, pady=10)
ttk.Button(button_frame, text='Update Existing Product', command=update_product).grid(row=0, column=1, padx=10, pady=10)
ttk.Button(button_frame, text='Delete Product', command=delete_product).grid(row=1, column=0, padx=10, pady=10)
ttk.Button(button_frame, text='Sell Product', command=sell_product).grid(row=1, column=1, padx=10, pady=10)

ttk.Button(button_frame, text='Show Inventory', command=show_inventory).grid(row=2, column=0, padx=10, pady=10)
ttk.Button(button_frame, text='Show Sales Report', command=generate_report).grid(row=2, column=1, padx=10, pady=10)
ttk.Button(button_frame, text='Save Inventory', command=save_inventory).grid(row=3, column=0, padx=10, pady=10)
ttk.Button(button_frame, text='Save Sales Data', command=save_sales).grid(row=3, column=1, padx=10, pady=10)

# Run the application
root.mainloop()
