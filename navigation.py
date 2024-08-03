import tkinter as tk
from tkinter import ttk

class NavigationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Navigation")
        self.root.geometry("400x200")

        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame, text="Select Application:", font=("Arial", 14)).pack(pady=10)

        self.app_list = ttk.Combobox(self.frame, values=[
            "To-Do List",
            "Notes",
            "Journal",
            "Goals",
            "Expenses"
        ])
        self.app_list.pack(pady=10)
        self.app_list.bind("<<ComboboxSelected>>", self.launch_app)

        self.launch_button = tk.Button(self.frame, text="Launch", command=self.launch_app, bg="#4CAF50", fg="white")
        self.launch_button.pack(pady=10)

    def launch_app(self, event=None):
        app_name = self.app_list.get()
        if app_name == "To-Do List":
            import todo_app
            todo_app.main()
        elif app_name == "Notes":
            import notes_app
            notes_app.main()
        elif app_name == "Journal":
            import journal_app
            journal_app.main()
        elif app_name == "Goals":
            import goals_app
            goals_app.main()
        elif app_name == "Expenses":
            import expense_app
            expense_app.main()
        else:
            tk.messagebox.showwarning("Selection Error", "Please select a valid application")

if __name__ == "__main__":
    root = tk.Tk()
    app = NavigationApp(root)
    root.mainloop()
