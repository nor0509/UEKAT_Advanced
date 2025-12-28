import json
import os
import uuid
import sqlite3
import pika
import requests
from flask import Flask, jsonify, request


app = Flask(__name__)

BASE_DIR = "/app/test_photo"
RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "task_queue"
DB_PATH = "/app/db/tasks.db"
UPLOAD_DIR = "/app/uploads"


def send_to_queue(task_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(task_data),  # tu przekazuje json z requesta
        properties=pika.BasicProperties(
            delivery_mode=2,  # tutaj zeby zapisac w rabbit jakby wywalilo
        ),
    )
    connection.close()


@app.route("/process/<filename>", methods=["GET"])
def process_request(filename):

    full_path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(full_path):
        return jsonify({f"error": f"Plik nie istnieje: {full_path}"}), 404

    task_id = str(uuid.uuid4())
    message = {"task_id": task_id, "full_path": full_path}
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = "INSERT INTO tasks (task_id, status, filename) VALUES (?, ?, ?)"
    values = (task_id, "PENDING", filename)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

    try:
        send_to_queue(message)

        return jsonify({"message": "Zadanie przyjęte do realizacji", "task_id": task_id, "status": "queued"}), 202
    except Exception as e:
        return jsonify({"error": f"Błąd kolejki: {str(e)}"}), 500


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/tasks/<task_id>", methods=["GET"])
def view_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = "SELECT task_id, status, result, filename, created_at from tasks where task_id = ?"
    value = (task_id,)
    cursor.execute(sql, value)
    row = cursor.fetchone()
    conn.close()

    if row:
        data = {"task_id": row[0], "status": row[1], "persons_detected": row[2], "file_name": row[3]}
        return jsonify(data)
    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks/all", methods=["GET"])
def view_all_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = "SELECT task_id, status, result, filename, created_at from tasks"
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    data = []
    for row in rows:
        if row:
            task = {"task_id": row[0], "status": row[1], "persons_detected": row[2], "file_name": row[3]}
            data.append(task)
    if data is None:
        return jsonify({"error": "Brak danych w bazie danych"})
    return jsonify(data)


@app.route("/api/count_people", methods=["GET"])
def count_people_get():
    img_url = request.args.get("url")

    if not img_url:
        return jsonify({"error": "Musisz podać parametr url"}), 400

    try:
        response = requests.get(img_url, timeout=10)
        task_id = str(uuid.uuid4())
        filename = f"url_{task_id}.jpg"
        full_path = os.path.join("/app/uploads", filename)

        with open(full_path, "wb") as f:
            f.write(response.content)
    except Exception as e:
        return jsonify({"error": f"Błąd pobierania: {e}"}), 400

    message = {"task_id": task_id, "full_path": full_path}
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = "INSERT INTO tasks (task_id, status, filename) VALUES (?, ?, ?)"
    values = (task_id, "PENDING", filename)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

    try:
        send_to_queue(message)

        return jsonify({"message": "Zadanie przyjęte do realizacji", "task_id": task_id, "status": "queued"}), 202
    except Exception as e:
        return jsonify({"error": f"Błąd kolejki: {str(e)}"}), 500


@app.route("/send_image", methods=["POST"])
def send_image():
    if "file" not in request.files:
        return jsonify({"error": "Brak części 'file' w żądadniu"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Nie wybrano pliku"})

    if file:
        try:
            ext = os.path.splitext(file.filename)[1]
            if not ext:
                ext = ".jpg"

            task_id = str(uuid.uuid4())
            safe_filename = f"upload_{task_id}{ext}"




            full_path = os.path.join(UPLOAD_DIR, safe_filename)

            file.save(full_path)

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task_id, status, filename) VALUES (?, ?, ?)", (task_id, "PENDING", safe_filename))
            conn.commit()
            conn.close()

            message = {"task_id": task_id, "full_path": full_path}
            send_to_queue(message)

            return jsonify({"message": "Plik przesłany i zakolejkowany", "task_id": task_id, "filename": safe_filename}), 202
        except Exception as e:
            return jsonify({"error": f"Błąd podczas zapisu: {str(e)}"}), 500


def init_db():
    os.makedirs("/app/db", exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            status TEXT,
            result INTEGER,
            filename TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
