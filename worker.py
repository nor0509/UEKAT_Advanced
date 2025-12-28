import json
import os
import sqlite3
import time
from detector import detect_objects
import pika


print("Czekam 10 sekund na start RabbitMQ...", flush=True)
time.sleep(10)

# stałe
BASE_DIR = "/app/uploads"
OUTPUT_DIR = "/app/processed"
RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "task_queue"
DB_PATH = "/app/db/tasks.db"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=True)


def callback(ch, method, properties, body):
    """
    # ch: kanał
    # method: informacje o dostarczeniu (np. tag)
    # properties: właściwości wiadomości
    # body: treść wiadomości (to co wysłało API)
    """

    data = json.loads(body)
    full_path = data["full_path"]
    task_id = data.get("task_id", None)

    print(f"Odebrano zadanie dla pliku {full_path} (ID: {task_id})", flush=True)

    output_filename = f"processed_{task_id}.jpg"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    try:
        count = detect_objects(full_path, output_path)
        print(f"Zakończono. Znaleziono osób: {count}", flush=True)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        sql = "UPDATE tasks SET status = ?, result = ? WHERE task_id = ?"
        values = ("COMPLETED", count, task_id)

        cursor.execute(sql, values)
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Błąd podczas realizacji procesu detect_objects:{e}", flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)  # przyjmujemy 1 msg do pracy
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)  # jak dostajemy msg to odpal callback
channel.start_consuming()  # uruchamiamy petle
