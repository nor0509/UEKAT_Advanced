import json
import os
import uuid

import pika
from flask import Flask, jsonify

app = Flask(__name__)

BASE_DIR = "/app/test_photo"
RABBITMQ_HOST = 'rabbitmq'
QUEUE_NAME = 'task_queue'

def send_to_queue(task_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(task_data), # tu przekazuje json z requesta
        properties=pika.BasicProperties(
            delivery_mode=2, # tutaj zeby zapisac w rabbit jakby wywalilo
        ))
    connection.close()


@app.route('/process/<filename>', methods=['GET'])
def process_request(filename):


    full_path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(full_path):
        return jsonify({f"error": f"Plik nie istnieje: {full_path}"}), 404

    task_id = str(uuid.uuid4())
    message = {
        "task_id": task_id,
        "filename": filename
    }

    try:
        send_to_queue(message)

        return jsonify({
            "message": "Zadanie przyjęte do realizacji",
            "task_id": task_id,
            "status": "queued"
        }), 202
    except Exception as e:
        return jsonify({"error": f"Błąd kolejki: {str(e)}"}), 500

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
