import os
import time
from flask import Flask, jsonify, request
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "appuser"),
        password=os.getenv("MYSQL_PASSWORD", "localdevpassword"),
        database=os.getenv("MYSQL_DATABASE", "taskmanager"),
        cursorclass=DictCursor,
        connect_timeout=5,
        autocommit=True,
    )

def wait_for_database():
    for attempt in range(1, 31):
        try:
            connection = get_connection()
            connection.close()
            print("Database connection successful.")
            return
        except Exception as exc:
            print(f"Waiting for database ({attempt}/30): {exc}")
            time.sleep(2)
    raise RuntimeError("Database did not become available in time.")

@app.get("/api/health")
def health():
    try:
        connection = get_connection()
        connection.close()
        return jsonify(status="ok", database="connected")
    except Exception:
        return jsonify(status="error", database="unavailable"), 503

@app.get("/api/tasks")
def list_tasks():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, created_at FROM tasks ORDER BY id DESC")
            tasks = cursor.fetchall()
        for task in tasks:
            task["created_at"] = task["created_at"].isoformat() if task["created_at"] else None
        return jsonify(tasks)
    finally:
        connection.close()

@app.post("/api/tasks")
def create_task():
    payload = request.get_json(silent=True) or {}
    title = str(payload.get("title", "")).strip()
    if not title:
        return jsonify(error="Task title is required."), 400
    if len(title) > 255:
        return jsonify(error="Task title must be 255 characters or fewer."), 400

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
            task_id = cursor.lastrowid
            cursor.execute(
                "SELECT id, title, created_at FROM tasks WHERE id = %s",
                (task_id,),
            )
            task = cursor.fetchone()
        task["created_at"] = task["created_at"].isoformat() if task["created_at"] else None
        return jsonify(task), 201
    finally:
        connection.close()

if __name__ == "__main__":
    wait_for_database()
    app.run(host="0.0.0.0", port=5000)
