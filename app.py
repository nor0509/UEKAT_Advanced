import os

from flask import Flask, jsonify

from detector import detect_objects

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FOLDER = os.path.join(BASE_DIR, "test_photo")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "results")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/local/<filename>", methods=["GET"])
def process_image(filename):
    full_path = os.path.join(SOURCE_FOLDER, filename)

    if not os.path.exists(full_path):
        return jsonify(
            {
                "error": "Plik nie istnieje",
                "path_checked": full_path,
            }
        )

    output_name = f"result_{filename}"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    try:
        count = detect_objects(full_path, output_path)

        return jsonify({"status": "success", "filename": filename, "people_count": count, "output_location": output_path}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
