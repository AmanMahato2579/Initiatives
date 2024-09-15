import tkinter as tk
from tkinter import messagebox
from todo_app import TODOApp
from notes_app import NotesApp
from journal_app import JournalApp
from goals_app import GoalTrackingApp
from expense_app import ExpenseApp

class NavigationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Initiatives")
        self.root.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.frame, text="Select Application:", font=("Arial", 14)).pack(pady=10)
        self.add_button("To-Do List", self.launch_todo_app)
        self.add_button("Notes", self.launch_notes_app)
        self.add_button("Journal", self.launch_journal_app)
        self.add_button("Goals", self.launch_goals_app)
        self.add_button("Expenses", self.launch_expense_app)

    def add_button(self, text, command):
        button = tk.Button(self.frame, text=text, command=command, bg="#4CAF50", fg="white")
        button.pack(pady=5, fill=tk.X)

    def launch_todo_app(self):
        self.launch_app(TODOApp, "To-Do List")

    def launch_notes_app(self):
        self.launch_app(NotesApp, "Notes")

    def launch_journal_app(self):
        self.launch_app(JournalApp, "Journal")

    def launch_goals_app(self):
        self.launch_app(GoalTrackingApp, "Goals")

    def launch_expense_app(self):
        self.launch_app(ExpenseApp, "Expenses")

    def launch_app(self, app_class, app_name):
        try:
            app_window = tk.Toplevel(self.root)
            app_class(app_window)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while launching the {app_name} application: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NavigationApp(root)
    root.mainloop()
