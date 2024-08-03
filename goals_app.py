import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from database import add_goal, get_completed_tasks, get_goals, update_goal, delete_goal, get_goal_by_id, update_goal_status

class GoalTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Goal Tracking App")
        self.root.geometry("700x500")

        self.create_widgets()
        self.load_goals()

    def create_widgets(self):
        self.root.configure(bg="#f0f0f0")

        # Main Layout Frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Goal Input Frame
        self.goal_input_frame = tk.Frame(self.main_frame, bg="#ffffff", padx=10, pady=10)
        self.goal_input_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(self.goal_input_frame, text="Goal:", bg="#ffffff", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.goal_entry = tk.Entry(self.goal_input_frame, width=40)
        self.goal_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.goal_input_frame, text="Details:", bg="#ffffff", anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.details_entry = tk.Text(self.goal_input_frame, width=40, height=5)
        self.details_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.goal_input_frame, text="Deadline (YYYY-MM-DD):", bg="#ffffff", anchor="w").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.deadline_entry = tk.Entry(self.goal_input_frame, width=40)
        self.deadline_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self.goal_input_frame, text="Add Goal", command=self.add_goal, bg="#4CAF50", fg="white").grid(row=3, columnspan=2, pady=10)

        # Goal List Frame
        self.goal_list_frame = tk.Frame(self.main_frame, bg="#f0f0f0", padx=10, pady=10)
        self.goal_list_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.goal_list_frame, text="Goals", bg="#f0f0f0", font=("Arial", 14, "bold")).pack(anchor="w", padx=10)
        self.goal_listbox = tk.Listbox(self.goal_list_frame, selectmode=tk.SINGLE, bg="#ffffff", selectbackground="#e0e0e0", activestyle="none", font=("Arial", 12), width=50, height=15)
        self.goal_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.goal_listbox.bind("<Double-1>", self.show_goal_details)

        # Buttons
        self.button_frame = tk.Frame(self.main_frame, bg="#f0f0f0", padx=10, pady=5)
        self.button_frame.pack(fill=tk.X, pady=5)

        tk.Button(self.button_frame, text="Edit Goal", command=self.edit_goal, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=7)
        tk.Button(self.button_frame, text="Delete Goal", command=self.delete_goal, bg="#F44336", fg="white").pack(side=tk.LEFT, padx=7)
        tk.Button(self.button_frame, text="Mark as Completed", command=self.mark_as_completed, bg="#FFC107", fg="black").pack(side=tk.LEFT, padx=7)
        tk.Button(self.button_frame, text="Show Completed Goals", command=self.load_completed_goals, bg="#9C27B0", fg="white").pack(side=tk.LEFT, padx=7)

    def add_goal(self):
        goal = self.goal_entry.get()
        details = self.details_entry.get("1.0", tk.END).strip()
        deadline = self.deadline_entry.get().strip()
        if not goal or not details or not deadline:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return
        try:
            add_goal(goal, details, deadline)
            self.load_goals()
            self.clear_goal_inputs()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD.")

    def clear_goal_inputs(self):
        self.goal_entry.delete(0, tk.END)
        self.details_entry.delete("1.0", tk.END)
        self.deadline_entry.delete(0, tk.END)

    def load_goals(self):
        self.goal_listbox.delete(0, tk.END)
        goals = get_goals()
        for goal in goals:
            self.goal_listbox.insert(tk.END, f"{goal[0]} | {goal[1]} | Deadline: {goal[3]}")

    def load_completed_goals(self):
        self.goal_listbox.delete(0, tk.END)
        goals = get_completed_tasks()
        for goal in goals:
            self.goal_listbox.insert(tk.END, f"{goal[0]} | {goal[1]} | Deadline: {goal[3]}")

    def show_goal_details(self, event):
        selected_index = self.goal_listbox.curselection()
        if not selected_index:
            return

        index = selected_index[0]
        goal_string = self.goal_listbox.get(index)
        goal_id = self.get_goal_id_from_string(goal_string)

        if not goal_id:
            messagebox.showerror("Error", "Goal details not found")
            return

        goal = get_goal_by_id(goal_id)
        if goal:
            goal_details = f"Goal: {goal[0]}\nDetails: {goal[1]}\nDeadline: {goal[2]}\nStatus: {'Completed' if goal[3] else 'Incomplete'}"
            messagebox.showinfo("Goal Details", goal_details)
        else:
            messagebox.showerror("Error", "Goal details not found")

    def get_goal_id_from_string(self, goal_string):
        parts = goal_string.split(" | ")
        if len(parts) > 0:
            return int(parts[0])
        return None

    def edit_goal(self):
        selected_index = self.goal_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select Goal", "Please select a goal to edit")
            return

        goal_string = self.goal_listbox.get(selected_index)
        goal_id = self.get_goal_id_from_string(goal_string)

        if not goal_id:
            messagebox.showerror("Error", "Goal details not found")
            return

        goal = get_goal_by_id(goal_id)
        if goal:
            new_goal = simpledialog.askstring("Edit Goal", "Enter new goal:", initialvalue=goal[0])
            new_details = simpledialog.askstring("Edit Goal", "Enter new details:", initialvalue=goal[1])
            new_deadline = simpledialog.askstring("Edit Goal", "Enter new deadline (YYYY-MM-DD):", initialvalue=goal[2])
            if new_goal and new_details and new_deadline:
                try:
                    update_goal(goal_id, new_goal, new_details, new_deadline)
                    self.load_goals()
                except ValueError:
                    messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD.")
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields")

    def delete_goal(self):
        selected_index = self.goal_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select Goal", "Please select a goal to delete")
            return

        goal_string = self.goal_listbox.get(selected_index)
        goal_id = self.get_goal_id_from_string(goal_string)

        if not goal_id:
            messagebox.showerror("Error", "Goal details not found")
            return

        delete_goal(goal_id)
        self.load_goals()

    def mark_as_completed(self):
        selected_index = self.goal_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select Goal", "Please select a goal to mark as completed")
            return

        goal_string = self.goal_listbox.get(selected_index)
        goal_id = self.get_goal_id_from_string(goal_string)

        if not goal_id:
            messagebox.showerror("Error", "Goal details not found")
            return

        update_goal_status(goal_id, 1)  # 1 indicates completed status
        self.load_goals()

if __name__ == "__main__":
    root = tk.Tk()
    app = GoalTrackingApp(root)
    root.mainloop()
