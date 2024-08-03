import sqlite3
from contextlib import contextmanager

# Database file paths
TASKS_DB_PATH = 'tasks.db'
NOTES_DB_PATH = 'notes.db'
EXPENSES_DB_PATH = 'expenses.db'
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
def create_expenses_table():
    """Create the expenses table."""
    query = """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL
    )
    """
    execute_query(EXPENSES_DB_PATH, query, commit=True)

def add_expense(description, amount, date):
    """Add a new expense."""
    query = 'INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)'
    execute_query(EXPENSES_DB_PATH, query, (description, amount, date), commit=True)

def get_expenses():
    """Retrieve all expenses."""
    query = 'SELECT * FROM expenses'
    return fetch_query(EXPENSES_DB_PATH, query)

def delete_expense(expense_id):
    """Delete an expense by ID."""
    query = 'DELETE FROM expenses WHERE id = ?'
    execute_query(EXPENSES_DB_PATH, query, (expense_id,), commit=True)

# Goals Setting
def create_goals_table():
    """Create the goals table."""
    query = """
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal TEXT NOT NULL,
        details TEXT NOT NULL,
        status INTEGER DEFAULT 0
    )
    """
    execute_query(GOALS_DB_PATH, query, commit=True)

def add_goal(goal, details):
    """Add a new goal."""
    query = 'INSERT INTO goals (goal, details) VALUES (?, ?)'
    execute_query(GOALS_DB_PATH, query, (goal, details), commit=True)

def get_goals():
    """Retrieve all goals."""
    query = 'SELECT * FROM goals'
    return fetch_query(GOALS_DB_PATH, query)

def update_goal(goal_id, new_goal, new_details):
    """Update an existing goal."""
    query = 'UPDATE goals SET goal = ?, details = ? WHERE id = ?'
    execute_query(GOALS_DB_PATH, query, (new_goal, new_details, goal_id), commit=True)

def delete_goal(goal_id):
    """Delete a goal by ID."""
    query = 'DELETE FROM goals WHERE id = ?'
    execute_query(GOALS_DB_PATH, query, (goal_id,), commit=True)

def get_goal_by_id(goal_id):
    """Retrieve a goal by its ID."""
    query = 'SELECT goal, details FROM goals WHERE id = ?'
    return fetch_query(GOALS_DB_PATH, query, (goal_id,))

def get_completed_goals():
    """Retrieve all completed goals."""
    query = 'SELECT * FROM goals WHERE status = 1'
    return fetch_query(GOALS_DB_PATH, query)

def update_goal_status(goal_id, new_status):
    """Update the status of a goal."""
    query = 'UPDATE goals SET status = ? WHERE id = ?'
    execute_query(GOALS_DB_PATH, query, (new_status, goal_id), commit=True)

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
