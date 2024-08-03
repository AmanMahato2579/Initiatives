import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class JournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Journal App")
        
        # Create UI elements
        self.title_label = tk.Label(root, text="Title:")
        self.title_label.pack(pady=5)
        
        self.title_entry = tk.Entry(root, width=50)
        self.title_entry.pack(pady=5)
        
        self.content_label = tk.Label(root, text="Content:")
        self.content_label.pack(pady=5)
        
        self.content_text = tk.Text(root, width=50, height=10)
        self.content_text.pack(pady=5)
        
        self.save_button = tk.Button(root, text="Save Entry", command=self.save_entry)
        self.save_button.pack(pady=5)
        
        self.view_button = tk.Button(root, text="View Entries", command=self.view_entries)
        self.view_button.pack(pady=5)
        
        self.delete_button = tk.Button(root, text="Delete Entry", command=self.delete_entry)
        self.delete_button.pack(pady=5)
        
        self.conn = sqlite3.connect('journal.db')
        self.create_table()
        
    def create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS journal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )''')
    
    def save_entry(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        if not title or not content:
            messagebox.showwarning("Input Error", "Please enter both title and content.")
            return
        
        with self.conn:
            self.conn.execute('INSERT INTO journal (title, content) VALUES (?, ?)', (title, content))
        messagebox.showinfo("Success", "Entry saved successfully!")
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)
    
    def view_entries(self):
        entries_window = tk.Toplevel(self.root)
        entries_window.title("Journal Entries")
        
        with self.conn:
            cursor = self.conn.execute('SELECT id, title FROM journal')
            entries = cursor.fetchall()
        
        listbox = tk.Listbox(entries_window, width=50, height=15)
        listbox.pack(pady=5)
        
        for entry in entries:
            listbox.insert(tk.END, f"ID: {entry[0]} - {entry[1]}")
        
        listbox.bind('<Double-1>', lambda e: self.show_entry_details(listbox.get(listbox.curselection()[0]), entries_window))
    
    def show_entry_details(self, entry_text, window):
        entry_id = int(entry_text.split(' - ')[0].split(': ')[1])
        with self.conn:
            cursor = self.conn.execute('SELECT title, content FROM journal WHERE id = ?', (entry_id,))
            entry = cursor.fetchone()
        
        details_window = tk.Toplevel(window)
        details_window.title(f"Entry {entry_id}")
        
        tk.Label(details_window, text=f"Title: {entry[0]}").pack(pady=5)
        tk.Text(details_window, width=50, height=10, wrap=tk.WORD).insert(tk.END, entry[1])
    
    def delete_entry(self):
        entry_id = simpledialog.askinteger("Delete Entry", "Enter the ID of the entry to delete:")
        if entry_id:
            with self.conn:
                self.conn.execute('DELETE FROM journal WHERE id = ?', (entry_id,))
            messagebox.showinfo("Success", "Entry deleted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = JournalApp(root)
    root.mainloop()
