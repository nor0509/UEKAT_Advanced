import sqlite3

import config


def init_db():
    config.ensure_directories()
    with get_db_connection() as conn:
        conn.execute(
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


def get_db_connection():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def insert_db_new_task(task_id, filename):
    with get_db_connection() as conn:
        sql = "INSERT INTO tasks (task_id, status, filename) VALUES (?, ?, ?)"
        conn.execute(sql, (task_id, "PENDING", filename))
        conn.commit()


def get_task_by_id(task_id):

    with get_db_connection() as conn:

        sql = "SELECT task_id, status, result, filename, created_at from tasks where task_id = ?"
        value = (task_id,)
        cursor = conn.execute(sql, value)
        row = cursor.fetchone()

    if row:
        return dict(row)
    return None


def get_all_tasks():
    with get_db_connection() as conn:
        sql = "SELECT task_id, status, result, filename, created_at from tasks"
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
    return [dict(row) for row in rows]


def update_db_task(count, task_id, is_error=False):
    with get_db_connection() as conn:
        if not is_error:
            sql = "UPDATE tasks SET status = ?, result = ? WHERE task_id = ?"
            values = ("COMPLETED", count, task_id)
        else:
            sql = "UPDATE tasks SET status = ?, result = NULL WHERE task_id = ?"
            values = ("ERROR", count, task_id)
        conn.execute(sql, values)
        conn.commit()
