import tkinter as tk
from tkinter import ttk, messagebox
import importlib
from services import *

class NavigationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Navigation")
        self.root.geometry("400x250")
        
        self.create_widgets()
        
    def create_widgets(self):
        self.frame = tk.Frame(self.root, padx=10, pady=10)  # Corrected padding options
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Title Label
        tk.Label(self.frame, text="Select Application", font=("Arial", 16, "bold")).pack(pady=20)

        # Combobox for selecting the application
        self.app_list = ttk.Combobox(self.frame, values=[
            "To-Do List",
            "Notes",
            "Journal",
            "Goals",
            "Expenses"
        ], state="readonly")
        self.app_list.pack(pady=10)
        self.app_list.bind("<<ComboboxSelected>>", self.enable_launch_button)

        # Launch Button
        self.launch_button = tk.Button(self.frame, text="Launch", command=self.launch_app, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.launch_button.pack(pady=20)
        self.launch_button.config(state=tk.DISABLED)

    def enable_launch_button(self, event=None):
        self.launch_button.config(state=tk.NORMAL)

    def launch_app(self, event=None):
        app_name = self.app_list.get()
        module_map = {
            "To-Do List": "services.tasks.todo_app",
            "Notes": "services.notes.notes_app",
            "Journal": "services.journal.journal_app",
            "Goals": "services.goals.goals_app",
            "Expenses": "services.expenses.expense_app"
        }

        module_name = module_map.get(app_name)
        if module_name:
            try:
                app_module = importlib.import_module(module_name)
                app_module.main()  # Ensure each module has a 'main' function
            except AttributeError:
                messagebox.showerror("Error", f"Module {app_name} does not have a main function.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch {app_name}: {str(e)}")
        else:
            messagebox.showwarning("Selection Error", "Please select a valid application")

if __name__ == "__main__":
    root = tk.Tk()
    app = NavigationApp(root)
    root.mainloop()
