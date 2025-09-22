import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime
import matplotlib.pyplot as plt

DATA_FILE = "expenses.json"

def load_expenses():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense():
    name = simpledialog.askstring("Expense Name", "Enter expense name:")
    if not name:
        return
    try:
        amount = float(simpledialog.askstring("Amount", "Enter amount ($):"))
    except (TypeError, ValueError):
        messagebox.showerror("Invalid Input", "Please enter a valid number for amount.")
        return
    category = simpledialog.askstring("Category", "Enter category (food, transport, etc.):")
    date = simpledialog.askstring("Date", "Enter date (YYYY-MM-DD) or leave blank for today:")
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    expenses = load_expenses()
    expenses.append({
        "name": name,
        "amount": amount,
        "category": category,
        "date": date
    })
    save_expenses(expenses)
    messagebox.showinfo("Success", "Expense added successfully!")
    update_listbox()

def update_listbox():
    expenses = load_expenses()
    expense_listbox.delete(0, tk.END)
    for i, expense in enumerate(expenses):
        expense_listbox.insert(
            tk.END, 
            f"{i+1}. {expense['date']} - {expense['name']} - ${expense['amount']} ({expense['category']})"
        )

def summarize_expenses():
    expenses = load_expenses()
    if not expenses:
        messagebox.showinfo("Summary", "No expenses to summarize.")
        return

    summary = {}
    for expense in expenses:
        cat = expense['category']
        summary[cat] = summary.get(cat, 0) + expense['amount']

    summary_text = "\n".join([f"{cat}: ${total:.2f}" for cat, total in summary.items()])
    messagebox.showinfo("Expense Summary", summary_text)

def plot_expenses():
    expenses = load_expenses()
    if not expenses:
        messagebox.showinfo("Plot", "No expenses to plot.")
        return

    summary = {}
    for expense in expenses:
        cat = expense['category']
        summary[cat] = summary.get(cat, 0) + expense['amount']

    categories = list(summary.keys())
    totals = list(summary.values())

    plt.figure(figsize=(8,5))
    plt.bar(categories, totals, color='skyblue')
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Amount ($)")
    plt.show()

# NEW: Delete expense
def delete_expense():
    selection = expense_listbox.curselection()
    if not selection:
        messagebox.showerror("Error", "Please select an expense to delete.")
        return
    
    index = selection[0]  # selected line index
    expenses = load_expenses()
    
    confirm = messagebox.askyesno("Confirm", f"Delete this expense?\n\n{expenses[index]}")
    if confirm:
        expenses.pop(index)
        save_expenses(expenses)
        update_listbox()

# NEW: Edit expense
def edit_expense():
    selection = expense_listbox.curselection()
    if not selection:
        messagebox.showerror("Error", "Please select an expense to edit.")
        return

    index = selection[0]
    expenses = load_expenses()
    expense = expenses[index]

    # Ask for new values (pre-fill old ones)
    name = simpledialog.askstring("Edit Name", "Enter expense name:", initialvalue=expense["name"])
    if not name:
        return
    try:
        amount = float(simpledialog.askstring("Edit Amount", "Enter amount ($):", initialvalue=str(expense["amount"])))
    except (TypeError, ValueError):
        messagebox.showerror("Invalid Input", "Please enter a valid number for amount.")
        return
    category = simpledialog.askstring("Edit Category", "Enter category:", initialvalue=expense["category"])
    date = simpledialog.askstring("Edit Date", "Enter date (YYYY-MM-DD):", initialvalue=expense["date"])

    # Save edited values
    expenses[index] = {
        "name": name,
        "amount": amount,
        "category": category,
        "date": date
    }
    save_expenses(expenses)
    messagebox.showinfo("Success", "Expense updated successfully!")
    update_listbox()

# GUI setup
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("600x500")

tk.Label(root, text="Expenses", font=("Helvetica", 14, "bold")).pack(pady=10)

expense_listbox = tk.Listbox(root, width=85)
expense_listbox.pack(pady=10)

tk.Button(root, text="Add Expense", command=add_expense, width=20, bg="lightgreen").pack(pady=5)
tk.Button(root, text="Edit Expense", command=edit_expense, width=20, bg="lightyellow").pack(pady=5)  # NEW
tk.Button(root, text="Delete Expense", command=delete_expense, width=20, bg="salmon").pack(pady=5)   # NEW
tk.Button(root, text="Summarize Expenses", command=summarize_expenses, width=20, bg="lightblue").pack(pady=5)
tk.Button(root, text="Plot Expenses", command=plot_expenses, width=20, bg="orange").pack(pady=5)
tk.Button(root, text="Exit", command=root.destroy, width=20, bg="tomato").pack(pady=5)

update_listbox()
root.mainloop()
