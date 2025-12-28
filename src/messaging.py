import time

import pika
import json
import config

def get_rabbitmq_connection():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=config.RABBITMQ_HOST)
            )
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ niegotowy. Czekam 5 sekund...", flush=True)
            time.sleep(5)

def send_to_queue(task_data):
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue=config.QUEUE_NAME, durable=True)

        channel.basic_publish(
            exchange="",
            routing_key=config.QUEUE_NAME,
            body=json.dumps(task_data),
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
        )
        connection.close()
        return True
    except Exception as e:
        print(f"Błąd RabbitMQ: {e}")
        raise e


def create_message(task_id, full_path):
    message = {"task_id": task_id, "full_path": full_path}
    return message

