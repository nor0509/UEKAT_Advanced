from flask_app.app.models.tag import Tag
import csv
import os
from flask_restful import Resource


class Tags(Resource):
    def get(self):
        tags_list = []
        file_path = os.path.join(os.getcwd(), "data/tags.csv")
        try:

            with open(file_path, mode="r", encoding="utf-8") as tags_file:
                reader = csv.DictReader(tags_file)
                # userId,movieId,tag,timestamp
                for row in reader:
                    tag_obj = Tag(
                        userId=row["userId"],
                        movieId=row["movieId"],
                        tag=row["tag"],
                        timestamp=row["timestamp"])
                    serialized_tag = tag_obj.__dict__

                    tags_list.append(serialized_tag)
                return tags_list
        except FileNotFoundError:
            return {"error": "brak pliku tags.csv"}, 404
