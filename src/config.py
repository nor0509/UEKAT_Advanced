import os.path

# const
OUTPUT_DIR = "/app/volumes/processed"
DB_DIR = "/app/volumes/db"
DB_NAME = "tasks.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)
MODEL_PATH = "/app/models/yolov8n.onnx"
UPLOAD_DIR = "/app/volumes/uploads"
LOCAL_IMG_DIR = "/app/volumes/local-img"

# rabbitmq
RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "task_queue"


def ensure_directories():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(DB_DIR, exist_ok=True)
