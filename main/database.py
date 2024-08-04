import sqlite3
from contextlib import contextmanager

# Database file paths
TASKS_DB_PATH = 'tasks.db'
NOTES_DB_PATH = 'notes.db'
EXPENSES_DB_PATH = 'Initiatives\services\expenses\expenses.db'
GOALS_DB_PATH = 'goals.db'
JOURNAL_DB_PATH = 'journal.db'

@contextmanager
def create_connection(db_path):
    """Create a database connection and ensure it is properly closed."""
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()

def execute_query(db_path, query, params=(), commit=False):
    """Execute a single query with optional commit."""
    try:
        with create_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if commit:
                conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def fetch_query(db_path, query, params=()):
    """Fetch data from the database."""
    try:
        with create_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []

# Task Management
def create_tasks_table():
    """Create the tasks table."""
    query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        priority TEXT NOT NULL,
        deadline TEXT NOT NULL,
        notes TEXT,
        status INTEGER NOT NULL DEFAULT 0
    )
    """
    execute_query(TASKS_DB_PATH, query, commit=True)
    
    # Create indexes
    index_queries = [
        'CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks (priority)',
        'CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks (status)'
    ]
    for index_query in index_queries:
        execute_query(TASKS_DB_PATH, index_query, commit=True)

def add_task(name, priority, deadline, notes='', status=0):
    """Add a new task."""
    query = 'INSERT INTO tasks (name, priority, deadline, notes, status) VALUES (?, ?, ?, ?, ?)'
    execute_query(TASKS_DB_PATH, query, (name, priority, deadline, notes, status), commit=True)

def get_tasks(status=0):
    """Retrieve all tasks with a given status."""
    query = 'SELECT id, name, priority, deadline FROM tasks WHERE status = ?'
    return fetch_query(TASKS_DB_PATH, query, (status,))

def update_task(task_id, name=None, priority=None, deadline=None, notes=None, status=None):
    """Update an existing task."""
    fields = {'name': name, 'priority': priority, 'deadline': deadline, 'notes': notes, 'status': status}
    updates = ', '.join(f"{key} = ?" for key, value in fields.items() if value is not None)
    params = [value for value in fields.values() if value is not None]
    params.append(task_id)
    if updates:
        query = f'UPDATE tasks SET {updates} WHERE id = ?'
        execute_query(TASKS_DB_PATH, query, params, commit=True)

def delete_task(task_id):
    """Delete a task by ID."""
    query = 'DELETE FROM tasks WHERE id = ?'
    execute_query(TASKS_DB_PATH, query, (task_id,), commit=True)

def get_task_by_id(task_id):
    """Retrieve a task by its ID."""
    query = 'SELECT * FROM tasks WHERE id = ?'
    return fetch_query(TASKS_DB_PATH, query, (task_id,))

def get_completed_tasks():
    """Retrieve all completed tasks."""
    query = 'SELECT id, name, priority, deadline FROM tasks WHERE status = 1'
    return fetch_query(TASKS_DB_PATH, query)

def get_missed_tasks():
    """Retrieve all missed tasks."""
    query = 'SELECT id, name, priority, deadline FROM tasks WHERE status = 2'
    return fetch_query(TASKS_DB_PATH, query)

# Notes Management
def create_notes_table():
    """Create the notes table."""
    query = """
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    )
    """
    execute_query(NOTES_DB_PATH, query, commit=True)

def save_notes(task_id, content):
    """Add notes for a specific task."""
    query = 'INSERT INTO notes (task_id, content) VALUES (?, ?)'
    execute_query(NOTES_DB_PATH, query, (task_id, content), commit=True)

def fetch_notes(task_id):
    """Retrieve notes for a specific task."""
    query = 'SELECT * FROM notes WHERE task_id = ?'
    return fetch_query(NOTES_DB_PATH, query, (task_id,))

def delete_notes(note_id):
    """Delete a note by ID."""
    query = 'DELETE FROM notes WHERE id = ?'
    execute_query(NOTES_DB_PATH, query, (note_id,), commit=True)

def update_note(note_id, new_content):
    """Update a note by ID."""
    query = 'UPDATE notes SET content = ? WHERE id = ?'
    execute_query(NOTES_DB_PATH, query, (new_content, note_id), commit=True)

# Expense Tracking
import sqlite3
from datetime import datetime

def connect():
    return sqlite3.connect('expenses.db')

def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            type TEXT,
            date TEXT,
            month INTEGER,
            year INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(description, amount, type, date, month, year):
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO expenses (description, amount, type, date, month, year)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (description, amount, type, date, month, year))
    conn.commit()
    conn.close()

def get_expenses(month, year):
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        SELECT * FROM expenses WHERE month = ? AND year = ?
    ''', (month, year))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_expenses_total(month, year):
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        SELECT SUM(amount) FROM expenses WHERE month = ? AND year = ? AND type = 'credit'
    ''', (month, year))
    credit_total = cur.fetchone()[0] or 0

    cur.execute('''
        SELECT SUM(amount) FROM expenses WHERE month = ? AND year = ? AND type = 'debit'
    ''', (month, year))
    debit_total = cur.fetchone()[0] or 0

    conn.close()
    return credit_total - debit_total

def delete_expense(expense_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM expenses WHERE id = ?
    ''', (expense_id,))
    conn.commit()
    conn.close()

def update_expense(expense_id, description, amount, type, date):
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        UPDATE expenses
        SET description = ?, amount = ?, type = ?, date = ?
        WHERE id = ?
    ''', (description, amount, type, date, expense_id))
    conn.commit()
    conn.close()

def get_expense_by_id(expense_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        SELECT description, amount, type, date FROM expenses WHERE id = ?
    ''', (expense_id,))
    expense = cur.fetchone()
    conn.close()
    return expense

# Goals Setting
import sqlite3

def create_tables():
    with sqlite3.connect("goals.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal TEXT NOT NULL,
                details TEXT NOT NULL,
                deadline DATE NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()

def add_goal(goal, details, deadline):
    with sqlite3.connect("goals.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO goals (goal, details, deadline) VALUES (?, ?, ?)", (goal, details, deadline))
        conn.commit()

def get_goals():
    with sqlite3.connect("goals.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, goal, details, deadline, completed FROM goals WHERE completed = 0")
        return cursor.fetchall()

def get_completed_tasks():
    with sqlite3.connect("goals.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, goal, details, deadline, completed FROM goals WHERE completed = 1")
        return cursor.fetchall()

def get_goal_by_id(goal_id):
    with sqlite3.connect("goals.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT goal, details, deadline, completed FROM goals WHERE id = ?", (goal_id,))
        return cursor.fetchone()

def update_goal(goal_id, new_goal, new_details, new_deadline):
    with sqlite3.connect("goals.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE goals SET goal = ?, details = ?, deadline = ? WHERE id = ?", (new_goal, new_details, new_deadline, goal_id))
        conn.commit()

def delete_goal(goal_id):
    with sqlite3.connect("goals.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
        conn.commit()

def update_goal_status(goal_id, status):
    with sqlite3.connect("goals.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE goals SET completed = ? WHERE id = ?", (status, goal_id))
        conn.commit()

# Daily Journaling
def create_journal_table():
    """Create the journal table."""
    query = """
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_date TEXT NOT NULL,
        entry TEXT NOT NULL
    )
    """
    execute_query(JOURNAL_DB_PATH, query, commit=True)

def add_journal_entry(entry_date, entry):
    """Add a new journal entry."""
    query = 'INSERT INTO journal (entry_date, entry) VALUES (?, ?)'
    execute_query(JOURNAL_DB_PATH, query, (entry_date, entry), commit=True)

def get_journal_entries():
    """Retrieve all journal entries."""
    query = 'SELECT * FROM journal'
    return fetch_query(JOURNAL_DB_PATH, query)

def update_journal_entry(entry_id, new_date, new_content):
    """Update an existing journal entry."""
    query = 'UPDATE journal SET entry_date = ?, entry = ? WHERE id = ?'
    execute_query(JOURNAL_DB_PATH, query, (new_date, new_content, entry_id), commit=True)

def delete_journal_entry(entry_id):
    """Delete a journal entry by ID."""
    query = 'DELETE FROM journal WHERE id = ?'
    execute_query(JOURNAL_DB_PATH, query, (entry_id,), commit=True)

#expense calculate
import sqlite3

# Function to create tables
def create_tables():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    amount REAL,
                    type TEXT,
                    date TEXT,
                    month INTEGER,
                    year INTEGER
                )''')
    conn.commit()
    conn.close()

# Function to add an expense
def add_expense(description, amount, type, date, month, year):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (description, amount, type, date, month, year) VALUES (?, ?, ?, ?, ?, ?)',
              (description, amount, type, date, month, year))
    conn.commit()
    conn.close()

# Function to get expenses by month and year
def get_expenses(month, year):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses WHERE month = ? AND year = ?', (month, year))
    expenses = c.fetchall()
    conn.close()
    return expenses

# Function to get total expenses by month and year
def get_expenses_total(month, year):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT SUM(amount) FROM expenses WHERE month = ? AND year = ?', (month, year))
    total = c.fetchone()[0]
    conn.close()
    return total if total is not None else 0.0

# Function to delete an expense by ID
def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()

# Function to get an expense by ID
def get_expense_by_id(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT description, amount, type, date FROM expenses WHERE id = ?', (expense_id,))
    expense = c.fetchone()
    conn.close()
    return expense

# Function to update an expense
def update_expense(expense_id, description, amount, type, date):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('UPDATE expenses SET description = ?, amount = ?, type = ?, date = ? WHERE id = ?',
              (description, amount, type, date, expense_id))
    conn.commit()
    conn.close()
