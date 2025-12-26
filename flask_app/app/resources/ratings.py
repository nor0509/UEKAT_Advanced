from flask_app.app.models.rating import Rating
import csv
import os
from flask_restful import Resource


class Ratings(Resource):
    def get(self):
        ratings_list = []
        file_path = os.path.join(os.getcwd(), "data/ratings.csv")
        try:

            with open(file_path, mode="r", encoding="utf-8") as ratings_file:
                reader = csv.DictReader(ratings_file)
                # userId,movieId,rating,timestamp
                for row in reader:
                    rating_obj = Rating(
                        userId=row["userId"],
                        movieId=row["movieId"],
                        rating=row["rating"],
                        timestamp=row["timestamp"])
                    serialized_rating = rating_obj.__dict__

                    ratings_list.append(serialized_rating)
                return ratings_list
        except FileNotFoundError:
            return {"error": "brak pliku rating.csv"}, 404
