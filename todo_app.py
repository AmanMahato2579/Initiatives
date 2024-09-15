import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkcalendar import DateEntry
from database import add_task, get_tasks, update_task, delete_task, get_task_by_id, get_completed_tasks, get_missed_tasks

class TODOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Initiatives")
        self.root.geometry("900x600")

        self.create_widgets()
        self.load_tasks()
        self.update_clock()

    def create_widgets(self):
        self.root.configure(bg="#f0f0f0")
        
        # Main Layout Frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Task Input Frame
        self.task_input_frame = tk.Frame(self.main_frame, bg="#ffffff", padx=10, pady=10)
        self.task_input_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(self.task_input_frame, text="Task Name:", bg="#ffffff", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.task_name_entry = tk.Entry(self.task_input_frame, width=40)
        self.task_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.task_input_frame, text="Priority:", bg="#ffffff", anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.priority_combobox = ttk.Combobox(self.task_input_frame, values=[
            "Supremacy", "Transcendence", "Antecedence", "Urgency", "Preference", "Inconsequential"])
        self.priority_combobox.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.task_input_frame, text="Deadline:", bg="#ffffff", anchor="w").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.deadline_entry = DateEntry(self.task_input_frame, date_pattern='dd/mm/yyyy')
        self.deadline_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.task_input_frame, text="Notes:", bg="#ffffff", anchor="w").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.notes_entry = tk.Entry(self.task_input_frame, width=40)
        self.notes_entry.grid(row=3, column=1, padx=5, pady=5)

        self.logo_label = tk.Label(self.task_input_frame, text="Initiatives: TODO LIST",
            font=("Arial", 16, "bold"), bg="#ffffff", fg="#333333")
        self.logo_label.grid(row=5, column=0, columnspan=2, pady=10, sticky="e")

        tk.Button(self.task_input_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white").grid(row=6, columnspan=2, pady=10)

        # Task List Frame
        self.task_list_frame = tk.Frame(self.main_frame, bg="#f0f0f0", padx=10, pady=10)
        self.task_list_frame.pack(fill=tk.BOTH, expand=True)

        # Incomplete Tasks
        tk.Label(self.task_list_frame, text="Incomplete Tasks", bg="#f0f0f0", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.incomplete_tasks_listbox = tk.Listbox(self.task_list_frame, selectmode=tk.SINGLE, bg="#ffffff", selectbackground="#FFFFED", activestyle="none", font=("Arial", 12), width=28, height=10)
        self.incomplete_tasks_listbox.grid(row=1, column=0, padx=10, pady=1, sticky="nsew")
        self.incomplete_tasks_listbox.bind("<Double-1>", self.show_notes)

        # Completed Tasks
        tk.Label(self.task_list_frame, text="Completed Tasks", bg="#f0f0f0", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.completed_tasks_listbox = tk.Listbox(self.task_list_frame, selectmode=tk.SINGLE, bg="#ffffff", selectbackground="#e0e0e0", activestyle="none", font=("Arial", 12), width=29, height=10)
        self.completed_tasks_listbox.grid(row=1, column=1, padx=10, pady=1, sticky="nsew")
        self.completed_tasks_listbox.bind("<Double-1>", self.show_notes)

        # Buttons
        self.button_frame = tk.Frame(self.main_frame, bg="#f0f0f0", padx=10, pady=5)
        self.button_frame.pack(fill=tk.X, pady=5)

        tk.Button(self.button_frame, text="Edit Task", command=self.edit_task, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=7)
        tk.Button(self.button_frame, text="Complete Task", command=self.complete_task, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=7)
        tk.Button(self.button_frame, text="Mark as Missed", command=self.mark_as_missed, bg="#9C27B0", fg="white").pack(side=tk.LEFT, padx=7)
        tk.Button(self.button_frame, text="Add Again", command=self.add_again, bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=7)
        tk.Button(self.button_frame, text="Clear Completed Tasks", command=self.clear_completed_tasks, bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=7)
        tk.Button(self.button_frame, text="Delete Task", command=self.delete_task, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=7)

        # Right Side (Clock and Missed Tasks)
        self.right_frame = tk.Frame(self.root, bg="#f0f0f0", width=300)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10, expand=False)

        # Clock
        self.clock_label = tk.Label(self.right_frame, text="", font=("Arial", 14), bg="#f0f0f0")
        self.clock_label.pack(pady=10)

        # Missed Tasks
        self.missed_tasks_frame = tk.Frame(self.right_frame, bg="#f0f0f0")
        self.missed_tasks_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.missed_tasks_frame, text="Missed Tasks", bg="#f0f0f0", font=("Arial", 14, "bold")).pack(anchor="w", padx=10)
        self.missed_tasks_listbox = tk.Listbox(self.missed_tasks_frame, bg="#ffffff", selectbackground="#e0e0e0", activestyle="none", font=("Arial", 12), width=40, height=15)
        self.missed_tasks_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.missed_tasks_listbox.bind("<Double-1>", self.show_notes)

    def add_task(self):
        name = self.task_name_entry.get()
        priority = self.priority_combobox.get()
        deadline = self.deadline_entry.get_date().strftime('%d/%m/%Y')
        notes = self.notes_entry.get()
        if not name or not priority:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return
        add_task(name, priority, deadline, notes)
        self.load_tasks()
        self.clear_task_inputs()

    def clear_task_inputs(self):
        self.task_name_entry.delete(0, tk.END)
        self.priority_combobox.set('')
        self.deadline_entry.set_date(datetime.date.today())
        self.notes_entry.delete(0, tk.END)

    def load_tasks(self):
        self.incomplete_tasks_listbox.delete(0, tk.END)
        self.completed_tasks_listbox.delete(0, tk.END)
        self.missed_tasks_listbox.delete(0, tk.END)

        incomplete_tasks = get_tasks(status=0)
        completed_tasks = get_completed_tasks()
        missed_tasks = get_missed_tasks()

        for task in incomplete_tasks:
            self.incomplete_tasks_listbox.insert(tk.END, f"{task[0]} | {task[1]} | {task[2]} | {task[3]}")

        for task in completed_tasks:
            self.completed_tasks_listbox.insert(tk.END, f"{task[0]} | {task[1]} | {task[2]} | {task[3]}")

        for task in missed_tasks:
            self.missed_tasks_listbox.insert(tk.END, f"{task[0]} | {task[1]} | {task[2]} | {task[3]}")

    def delete_task(self):
        selected_index = self.incomplete_tasks_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select Task", "Please select a task to delete")
            return

        task_string = self.incomplete_tasks_listbox.get(selected_index)
        task_id = self.get_task_id_from_string(task_string)

        if not task_id:
            messagebox.showerror("Error", "Task details not found")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            delete_task(task_id)
            self.load_tasks()

    def show_notes(self, event):
        selected_listbox = event.widget
        selection = selected_listbox.curselection()
        if not selection:
            print("No selection made in the listbox.")
            return

        index = selection[0]
        task_string = selected_listbox.get(index)
        task_id = self.get_task_id_from_string(task_string)

        if not task_id:
            messagebox.showerror("Error", "Task details not found")
            return

        task = get_task_by_id(task_id)
        if task:
            task_details = f"Task Name: {task[0]}\nPriority: {task[1]}\nDeadline: {task[2]}\nNotes: {task[3]}"
            messagebox.showinfo("Task Details", task_details)
        else:
            messagebox.showerror("Error", "Task details not found")

    def get_task_id_from_string(self, task_string):
        parts = task_string.split(" | ")
        if len(parts) > 0:
            try:
                return int(parts[0])
            except ValueError:
                return None
        return None

    def edit_task(self):
        selected_index = self.incomplete_tasks_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select Task", "Please select a task to edit")
            return

        task_string = self.incomplete_tasks_listbox.get(selected_index)
        task_id = self.get_task_id_from_string(task_string)

        if not task_id:
            messagebox.showerror("Error", "Task details not found")
            return

        task = get_task_by_id(task_id)
        if task:
            new_name = simpledialog.askstring("Edit Task", "Enter new task name:", initialvalue=task[0])
            new_priority = simpledialog.askstring("Edit Task", "Enter new priority:", initialvalue=task[1])
            new_deadline = simpledialog.askstring("Edit Task", "Enter new deadline (dd/mm/yyyy):", initialvalue=task[2])
            new_notes = simpledialog.askstring("Edit Task", "Enter new notes:", initialvalue=task[3])
            if new_name and new_priority and new_deadline and new_notes:
                update_task(task_id, new_name, new_priority, new_deadline, new_notes)
                self.load_tasks()
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields")

    def complete_task(self):
        selected_index = self.incomplete_tasks_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select Task", "Please select a task to complete")
            return

        task_string = self.incomplete_tasks_listbox.get(selected_index)
        task_id = self.get_task_id_from_string(task_string)

        if not task_id:
            messagebox.showerror("Error", "Task details not found")
            return

        update_task(task_id, status=1)
        self.load_tasks()

    def mark_as_missed(self):
        selected_index = self.incomplete_tasks_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select Task", "Please select a task to mark as missed")
            return

        task_string = self.incomplete_tasks_listbox.get(selected_index)
        task_id = self.get_task_id_from_string(task_string)

        if not task_id:
            messagebox.showerror("Error", "Task details not found")
            return

        update_task(task_id, status=2)
        self.load_tasks()

    def add_again(self):
        selected_index = self.completed_tasks_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select Task", "Please select a task to add again")
            return

        task_string = self.completed_tasks_listbox.get(selected_index)
        task_id = self.get_task_id_from_string(task_string)

        if not task_id:
            messagebox.showerror("Error", "Task details not found")
            return

        task = get_task_by_id(task_id)
        if task:
            name = task[0]
            priority = task[1]
            deadline = task[2]
            notes = task[3]
            add_task(name, priority, deadline, notes)
            update_task(task_id, status=0)
            self.load_tasks()
        else:
            messagebox.showerror("Error", "Task details not found")

    def clear_completed_tasks(self):
        completed_tasks = get_completed_tasks()
        for task in completed_tasks:
            delete_task(task[0])
        self.load_tasks()

    def update_clock(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)  # Update the clock every second
        
def main():
    root = tk.Tk()
    app = TODOApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
