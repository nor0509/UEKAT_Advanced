import json
import os
from detector import detect_objects
import config
from database import update_db_task
from messaging import get_rabbitmq_connection

connection = get_rabbitmq_connection()
channel = connection.channel()
channel.queue_declare(queue=config.QUEUE_NAME, durable=True)


def callback(ch, method, properties, body):

    data = json.loads(body)
    full_path = data["full_path"]
    task_id = data.get("task_id", None)

    print(f"Odebrano zadanie dla pliku {full_path} (ID: {task_id})", flush=True)

    output_filename = f"processed_{task_id}.jpg"
    output_path = os.path.join(config.OUTPUT_DIR, output_filename)

    try:
        count = detect_objects(full_path, output_path)
        print(f"Zakończono. Znaleziono osób: {count}", flush=True)

        update_db_task(count, task_id)

    except Exception as e:
        print(f"Błąd podczas realizacji procesu detect_objects:{e}", flush=True)
        if task_id:
            update_db_task(None, task_id, is_error=True)

    ch.basic_ack(delivery_tag=method.delivery_tag) #zmienaimy tag nawet jak error, bo by kolejkował w nieskończoność


channel.basic_qos(prefetch_count=1)  # przyjmujemy 1 msg do pracy
print('Działam i oczekuję...', flush=True)
channel.basic_consume(queue=config.QUEUE_NAME, on_message_callback=callback)  # jak dostajemy msg to odpal callback

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Zatrzymywanie workera...")
    connection.close()
