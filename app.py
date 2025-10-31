from flask import Flask, render_template, request, redirect, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Connect to SQLite using absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "tasks.db")
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS TASK (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT
)
""")
conn.commit()

# Home route - show all tasks
@app.route('/')
def home():
    cursor.execute("SELECT * FROM TASK")
    tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks)

# Add task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    cursor.execute("INSERT INTO TASK (title, description, status) VALUES (?, ?, ?)", (title, description, status))
    conn.commit()
    flash("Task added successfully!")
    return redirect('/')

# Edit task - show edit form
@app.route('/edit/<int:id>')
def edit_task(id):
    cursor.execute("SELECT * FROM TASK WHERE id = ?", (id,))
    task = cursor.fetchone()
    return render_template("edit.html", task=task)

# Update task - save changes
@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    cursor.execute("UPDATE TASK SET title=?, description=?, status=? WHERE id=?", (title, description, status, id))
    conn.commit()
    flash("Task updated successfully!")
    return redirect('/')

# Delete task
@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    cursor.execute("DELETE FROM TASK WHERE id = ?", (id,))
    conn.commit()
    flash("Task deleted successfully!")
    return redirect('/')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT COUNT(*) FROM TASK WHERE status = 'Pending'")
    pending = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM TASK WHERE status = 'Completed'")
    completed = cursor.fetchone()[0]

    # Ensure chart has at least one slice
    if pending == 0 and completed == 0:
        pending = 1
        completed = 0

    return render_template("dashboard.html", pending=pending, completed=completed)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS TASK (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT,
    employee TEXT,
    role TEXT
)
""")

