import os
import uuid
import requests
import config
from flask import jsonify, request, Blueprint
from messaging import send_to_queue, create_message
from database import get_task_by_id, get_all_tasks, insert_db_new_task

#sciaga
#200 OK
#202 Accepted (do kolejki)
#400 Bad Request
#404 Not Found
#500 Internal Server Error



api = Blueprint("api", __name__)


@api.route("/")
def main():
    return """
    <h2>Lista Endpointów API</h2>
    <h4>RabbitMQ: <a href="http://localhost:15672/">http://localhost:15672/</a></h4>
    <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px;">Metoda</th>
                <th style="padding: 8px;">Endpoint</th>
                <th style="padding: 8px;">Opis</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding: 8px;">GET</td>
                <td style="padding: 8px;">/tasks</td>
                <td style="padding: 8px;">Lista wszystkich zadań</td>
            </tr>
            <tr>
                <td style="padding: 8px;">GET</td>
                <td style="padding: 8px;">/tasks/&lt;id&gt;</td>
                <td style="padding: 8px;">Szczegóły konkretnego zadania</td>
            </tr>
            <tr>
                <td style="padding: 8px;">POST</td>
                <td style="padding: 8px;">/tasks/upload</td>
                <td style="padding: 8px;">Upload pliku (form-data: 'file')</td>
            </tr>
            <tr>
                <td style="padding: 8px;">GET</td>
                <td style="padding: 8px;">/tasks/process-url?url=...</td>
                <td style="padding: 8px;">Przetwarzanie z linku URL</td>
            </tr>
            <tr>
                <td style="padding: 8px;">GET</td>
                <td style="padding: 8px;">/tasks/process-local/&lt;plik&gt;</td>
                <td style="padding: 8px;">Przetwarzanie pliku lokalnego</td>
            </tr>
        </tbody>
    </table>
    """


@api.route("/tasks/process-local/<filename>", methods=["GET"])
def create_task_local(filename):

    full_path = os.path.join(config.LOCAL_IMG_DIR, filename)

    if not os.path.exists(full_path):
        return jsonify({f"error": f"Plik nie istnieje: {full_path}"}), 404

    task_id = str(uuid.uuid4())

    insert_db_new_task(task_id, filename)

    message = create_message(task_id, full_path)
    try:
        send_to_queue(message)

        return jsonify({"message": "Zadanie przyjęte do realizacji", "task_id": task_id, "status": "queued"}), 202
    except Exception as e:
        return jsonify({"error": f"Błąd kolejki: {str(e)}"}), 500

#zrobiłbym tu post, ale wymagania jasno wskazują na get
@api.route("/tasks/process-url", methods=["GET"])
def create_task_url():
    img_url = request.args.get("url")

    if not img_url:
        return jsonify({"error": "Musisz podać parametr url"}), 400

    try:
        response = requests.get(img_url, timeout=10)
        task_id = str(uuid.uuid4())
        filename = f"url_{task_id}.jpg"
        full_path = os.path.join(config.UPLOAD_DIR, filename)

        with open(full_path, "wb") as f:
            f.write(response.content)
    except Exception as e:
        return jsonify({"error": f"Błąd pobierania: {e}"}), 400

    message = create_message(task_id, full_path)

    insert_db_new_task(task_id, filename)

    try:
        send_to_queue(message)

        return jsonify({
            "message": "Zadanie przyjęte do realizacji",
            "task_id": task_id,
            "status": "queued"}), 202
    except Exception as e:
        return jsonify({"error": f"Błąd kolejki: {str(e)}"}), 500


@api.route("/tasks/upload", methods=["POST"])
def create_task_upload():
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

            filename = f"upload_{task_id}_{ext}"

            full_path = os.path.join(config.UPLOAD_DIR, filename)

            file.save(full_path)

            insert_db_new_task(task_id, filename)

            message = create_message(task_id, full_path)
            send_to_queue(message)

            return jsonify({
                "message": "Plik przesłany i zakolejkowany",
                "task_id": task_id,
                "filename": filename}), 202
        except Exception as e:
            return jsonify({"error": f"Błąd podczas zapisu: {str(e)}"}), 500


@api.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = get_task_by_id(task_id)
    if task:
        return jsonify(task)
    return jsonify({"error": "Nie znaleziono zadania"}), 404


@api.route("/tasks/", methods=["GET"])
def get_tasks():
    tasks = get_all_tasks()
    if tasks:
        return jsonify(tasks)
    return jsonify({"error": "Brak danych"}), 200
