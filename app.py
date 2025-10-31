from flask import Flask, render_template, request, redirect, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# -------------------- DATABASE SETUP --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "tasks.db")
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

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
conn.commit()

# -------------------- ROUTES --------------------

@app.route('/')
def home():
    cursor.execute("SELECT * FROM TASK")
    tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    employee = request.form['employee']
    role = request.form['role']

    cursor.execute("""
        INSERT INTO TASK (title, description, status, employee, role)
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, status, employee, role))
    conn.commit()

    flash("✅ Task added successfully!")
    return redirect('/')

@app.route('/edit/<int:id>')
def edit_task(id):
    cursor.execute("SELECT * FROM TASK WHERE id = ?", (id,))
    task = cursor.fetchone()
    if task:
        return render_template("edit.html", task=task)
    else:
        flash("⚠️ Task not found.")
        return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    employee = request.form['employee']
    role = request.form['role']

    cursor.execute("""
        UPDATE TASK SET title=?, description=?, status=?, employee=?, role=? WHERE id=?
    """, (title, description, status, employee, role, id))
    conn.commit()

    flash("✏️ Task updated successfully!")
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    cursor.execute("DELETE FROM TASK WHERE id = ?", (id,))
    conn.commit()
    flash("🗑️ Task deleted successfully!")
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT COUNT(*) FROM TASK WHERE status = 'Pending'")
    pending = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM TASK WHERE status = 'Completed'")
    completed = cursor.fetchone()[0]

    cursor.execute("SELECT role, COUNT(*) FROM TASK GROUP BY role")
    role_summary = dict(cursor.fetchall())

    cursor.execute("SELECT employee, COUNT(*) FROM TASK GROUP BY employee")
    employee_data = cursor.fetchall()
    employees = [{"name": row[0], "task_count": row[1]} for row in employee_data if row[0]]

    # Prevent chart crash if no data
    if pending == 0 and completed == 0:
        pending = 1
        completed = 0

    return render_template(
        "dashboard.html",
        pending=pending,
        completed=completed,
        role_summary=role_summary,
        employees=employees
    )

# -------------------- RUN --------------------
if __name__ == '__main__':
    app.run(debug=True)
