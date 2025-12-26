from flask_app.app.models.movie import Movie
import csv
import os
from flask_restful import Resource


class Movies(Resource):
    def get(self):
        movies_list = []

        file_path = os.path.join(os.getcwd(), "data/movies.csv")

        try:
            with open(file_path, mode="r", encoding="utf-8") as movies_file:
                reader = csv.DictReader(movies_file)

                for row in reader:
                    movie_obj = Movie(
                        id=row["movieId"],
                        title=row["title"],
                        genres=row["genres"])

                    serialized_movie = movie_obj.__dict__

                    movies_list.append(serialized_movie)
            return movies_list
        except FileNotFoundError:
            return {"error": "brak pliku movies.csv"}, 404
