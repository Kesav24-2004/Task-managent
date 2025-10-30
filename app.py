from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Connect to SQLite
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
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
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks)

# Add task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    cursor.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)", (title, description, status))
    conn.commit()
    return redirect('/')

# Edit task - show edit form
@app.route('/edit/<int:id>')
def edit_task(id):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    task = cursor.fetchone()
    return render_template("edit.html", task=task)

# Update task - save changes
@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    cursor.execute("UPDATE tasks SET title=?, description=?, status=? WHERE id=?", (title, description, status, id))
    conn.commit()
    return redirect('/')

# Delete task
@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    return redirect('/')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Pending'")
    pending = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Completed'")
    completed = cursor.fetchone()[0]
    return render_template("dashboard.html", pending=pending, completed=completed)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
