from flask_app.app.models.link import Link
import csv
import os
from flask_restful import Resource


class Links(Resource):
    def get(self):
        links_list = []
        file_path = os.path.join(os.getcwd(), "data/links.csv")
        try:

            with open(file_path, mode="r", encoding="utf-8") as links_file:
                reader = csv.DictReader(links_file)

                for row in reader:
                    link_obj = Link(
                        movieId=row["movieId"],
                        imdbId=row["imdbId"],
                        tmdbId=row["tmdbId"])
                    serialized_link = link_obj.__dict__

                    links_list.append(serialized_link)
                return links_list
        except FileNotFoundError:
            return {"error": "brak pliku links.csv"}, 404
