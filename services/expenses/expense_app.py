import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
from database import add_expense, get_expenses, get_expenses_total, delete_expense, update_expense, get_expense_by_id, create_tables

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x400")

        self.create_widgets()
        self.load_expenses()

    def create_widgets(self):
        self.root.configure(bg="#f0f0f0")

        # Main Layout Frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Expense Input Frame
        self.expense_input_frame = tk.Frame(self.main_frame, bg="#ffffff", padx=10, pady=10)
        self.expense_input_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(self.expense_input_frame, text="Description:", bg="#ffffff", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = tk.Entry(self.expense_input_frame, width=40)
        self.description_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.expense_input_frame, text="Amount:", bg="#ffffff", anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = tk.Entry(self.expense_input_frame, width=40)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.expense_input_frame, text="Type:", bg="#ffffff", anchor="w").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.type_var = tk.StringVar(value="credit")
        tk.Radiobutton(self.expense_input_frame, text="Credit", variable=self.type_var, value="credit", bg="#ffffff").grid(row=2, column=1, padx=5, pady=5, sticky="w")
        tk.Radiobutton(self.expense_input_frame, text="Debit", variable=self.type_var, value="debit", bg="#ffffff").grid(row=2, column=1, padx=5, pady=5)

        # Set the date field to the current date
        self.current_date = datetime.now().strftime("%d/%m/%Y")
        tk.Label(self.expense_input_frame, text=f"Date: {self.current_date}", bg="#ffffff", anchor="w").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = tk.Entry(self.expense_input_frame, width=40)
        self.date_entry.insert(0, self.current_date)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.expense_input_frame, text="Add Expense", command=self.add_expense, bg="#4CAF50", fg="white").grid(row=4, columnspan=2, pady=10)

        # Expense List Frame
        self.expense_list_frame = tk.Frame(self.main_frame, bg="#f0f0f0", padx=10, pady=10)
        self.expense_list_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.expense_list_frame, text="Expenses", bg="#f0f0f0", font=("Arial", 14, "bold")).pack(anchor="w", padx=10)

        self.month_frame = tk.Frame(self.expense_list_frame, bg="#f0f0f0")
        self.month_frame.pack(padx=10, pady=5, fill=tk.X)

        self.expense_listbox = tk.Listbox(self.month_frame, selectmode=tk.SINGLE, bg="#ffffff", selectbackground="#e0e0e0", activestyle="none", font=("Arial", 12), width=50, height=15)
        self.expense_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.expense_listbox.bind("<Double-1>", self.show_expense_details)

        # Buttons
        self.button_frame = tk.Frame(self.expense_list_frame, bg="#f0f0f0", padx=10, pady=5)
        self.button_frame.pack(fill=tk.X, pady=5)

        tk.Button(self.button_frame, text="Edit Expense", command=self.edit_expense, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=7)
        tk.Button(self.button_frame, text="Delete Expense", command=self.delete_expense, bg="#F44336", fg="white").pack(side=tk.LEFT, padx=7)

        # Total Expenses Label
        self.total_label = tk.Label(self.main_frame, text="Total Savings: $0.00", bg="#f0f0f0", font=("Arial", 12, "bold"))
        self.total_label.pack(pady=10)

    def add_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        type = self.type_var.get()
        date = self.date_entry.get()
        if not description or not amount or not date:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a number")
            return
        month = datetime.now().month
        year = datetime.now().year
        add_expense(description, amount, type, date, month, year)
        self.load_expenses()
        self.clear_expense_inputs()

    def clear_expense_inputs(self):
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

    def load_expenses(self):
        self.expense_listbox.delete(0, tk.END)
        self.month_frame.pack_forget()  # Hide the listbox while updating
        self.month_frame = tk.Frame(self.expense_list_frame, bg="#f0f0f0")
        self.month_frame.pack(padx=10, pady=5, fill=tk.X)
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        for i, month in enumerate(months):
            btn = tk.Button(self.month_frame, text=month, command=lambda m=i+1: self.show_expenses_by_month(m), bg="#ffffff", font=("Arial", 12), width=15)
            btn.pack(pady=2)
        self.update_total_savings()

    def show_expenses_by_month(self, month):
        self.expense_listbox.delete(0, tk.END)
        year = datetime.now().year
        expenses = get_expenses(month, year)
        for expense in expenses:
            expense_text = f"{expense[1]} - ${expense[2]:.2f} - {expense[3]} - {expense[4]} - ID:{expense[0]}"
            self.expense_listbox.insert(tk.END, expense_text)
        self.expense_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def update_total_savings(self):
        month = datetime.now().month
        year = datetime.now().year
        total_savings = get_expenses_total(month, year)
        self.total_label.config(text=f"Total Savings: ${total_savings:.2f}")

    def show_expense_details(self, event):
        selected_index = self.expense_listbox.curselection()
        if not selected_index:
            return
        expense_text = self.expense_listbox.get(selected_index)
        expense_id = self.get_expense_id(expense_text)
        if expense_id:
            expense_details = get_expense_by_id(expense_id)
            if expense_details:
                messagebox.showinfo("Expense Details", f"Description: {expense_details[0]}\nAmount: ${expense_details[1]:.2f}\nType: {expense_details[2]}\nDate: {expense_details[3]}")

    def get_expense_id(self, expense_text):
        # Extracting the ID from the expense text
        parts = expense_text.split(" - ID:")
        if len(parts) > 1:
            return int(parts[1])
        return None

    def edit_expense(self):
        selected_index = self.expense_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select an expense to edit")
            return
        expense_text = self.expense_listbox.get(selected_index)
        expense_id = self.get_expense_id(expense_text)
        if expense_id:
            expense_details = get_expense_by_id(expense_id)
            if expense_details:
                new_description = simpledialog.askstring("Edit Description", "New Description:", initialvalue=expense_details[0])
                new_amount = simpledialog.askfloat("Edit Amount", "New Amount:", initialvalue=expense_details[1])
                new_type = simpledialog.askstring("Edit Type", "New Type (credit/debit):", initialvalue=expense_details[2])
                new_date = simpledialog.askstring("Edit Date", "New Date (dd/mm/yyyy):", initialvalue=expense_details[3])
                if new_description and new_amount is not None and new_type and new_date:
                    update_expense(expense_id, new_description, new_amount, new_type, new_date)
                    self.load_expenses()
                    self.update_total_savings()
                else:
                    messagebox.showwarning("Input Error", "All fields must be filled in")

    def delete_expense(self):
        selected_index = self.expense_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select an expense to delete")
            return
        expense_text = self.expense_listbox.get(selected_index)
        expense_id = self.get_expense_id(expense_text)
        if expense_id:
            delete_expense(expense_id)
            self.load_expenses()
            self.update_total_savings()

if __name__ == "__main__":
    root = tk.Tk()
    create_tables()
    app = ExpenseApp(root)
    root.mainloop()
