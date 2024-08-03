import tkinter as tk
from tkinter import messagebox, simpledialog
from database import save_notes, fetch_notes, update_note, delete_notes, create_notes_table

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes")
        self.root.geometry("600x400")

        create_notes_table()  # Ensure the notes table is created

        self.create_widgets()
        self.load_notes()

    def create_widgets(self):
        self.root.configure(bg="#f0f0f0")

        # Main Layout Frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Note Input Frame
        self.note_input_frame = tk.Frame(self.main_frame, bg="#ffffff", padx=10, pady=10)
        self.note_input_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(self.note_input_frame, text="Note Title:", bg="#ffffff", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.note_title_entry = tk.Entry(self.note_input_frame, width=40)
        self.note_title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.note_input_frame, text="Note Content:", bg="#ffffff", anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.note_content_entry = tk.Text(self.note_input_frame, width=40, height=10)
        self.note_content_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.note_input_frame, text="Add Note", command=self.add_note, bg="#4CAF50", fg="white").grid(row=2, columnspan=2, pady=10)

        # Note List Frame
        self.note_list_frame = tk.Frame(self.main_frame, bg="#f0f0f0", padx=10, pady=10)
        self.note_list_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.note_list_frame, text="Notes", bg="#f0f0f0", font=("Arial", 14, "bold")).pack(anchor="w", padx=10)
        self.note_listbox = tk.Listbox(self.note_list_frame, selectmode=tk.SINGLE, bg="#ffffff", selectbackground="#e0e0e0", activestyle="none", font=("Arial", 12), width=50, height=15)
        self.note_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.note_listbox.bind("<Double-1>", self.show_note_details)

        # Buttons
        self.button_frame = tk.Frame(self.main_frame, bg="#f0f0f0", padx=10, pady=5)
        self.button_frame.pack(fill=tk.X, pady=5)

        tk.Button(self.button_frame, text="Edit Note", command=self.edit_note, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=7)
        tk.Button(self.button_frame, text="Delete Note", command=self.delete_note, bg="#F44336", fg="white").pack(side=tk.LEFT, padx=7)

    def add_note(self):
        title = self.note_title_entry.get()
        content = self.note_content_entry.get("1.0", tk.END).strip()
        if not title or not content:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return
        task_id = 1  # Example task_id, replace with actual task_id
        save_notes(task_id, content)
        self.load_notes()
        self.clear_note_inputs()

    def clear_note_inputs(self):
        self.note_title_entry.delete(0, tk.END)
        self.note_content_entry.delete("1.0", tk.END)

    def load_notes(self):
        self.note_listbox.delete(0, tk.END)
        task_id = 1  # Example task_id, replace with actual task_id
        notes = fetch_notes(task_id)
        for note in notes:
            self.note_listbox.insert(tk.END, f"{note[0]} | {note[2]}")  # Displaying id and content

    def show_note_details(self, event):
        selected_index = self.note_listbox.curselection()
        if not selected_index:
            return

        index = selected_index[0]
        note_string = self.note_listbox.get(index)
        note_id = self.get_note_id_from_string(note_string)

        if not note_id:
            messagebox.showerror("Error", "Note details not found")
            return

        note = fetch_notes(note_id)  # This should be modified if `fetch_notes` does not return the note directly
        if note:
            note_details = f"Note Title: {note[0]}\nContent: {note[2]}"
            messagebox.showinfo("Note Details", note_details)
        else:
            messagebox.showerror("Error", "Note details not found")

    def get_note_id_from_string(self, note_string):
        parts = note_string.split(" | ")
        if len(parts) > 0:
            return int(parts[0])
        return None

    def edit_note(self):
        selected_index = self.note_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select Note", "Please select a note to edit")
            return

        note_string = self.note_listbox.get(selected_index)
        note_id = self.get_note_id_from_string(note_string)

        if not note_id:
            messagebox.showerror("Error", "Note details not found")
            return

        note = fetch_notes(note_id)  # This should be modified if `fetch_notes` does not return the note directly
        if note:
            new_content = simpledialog.askstring("Edit Note", "Enter new note content:", initialvalue=note[2])
            if new_content:
                update_note(note_id, new_content)
                self.load_notes()
            else:
                messagebox.showwarning("Input Error", "Note content cannot be empty")

    def delete_note(self):
        selected_index = self.note_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Select Note", "Please select a note to delete")
            return

        note_string = self.note_listbox.get(selected_index)
        note_id = self.get_note_id_from_string(note_string)

        if not note_id:
            messagebox.showerror("Error", "Note details not found")
            return

        delete_notes(note_id)
        self.load_notes()

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
