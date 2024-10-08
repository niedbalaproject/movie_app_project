import json
import os
from istorage import IStorage


class StorageJson(IStorage):
    """
    IStorage interface implementation for storing movie data.
    """

    def __init__(self, file_path):
        """
        Initialize the StorageJson instance.

        Args:
            file_path (str): The path to the JSON file.
        """
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as handle:
                json.dump({}, handle)

    def _read_storage(self):
        """Reads the JSON storage file and returns the data."""
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _write_storage(self, data):
        """Writes data to the JSON storage file."""
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def list_movies(self):
        """List all movies from storage."""
        return self._read_storage()

    def add_movie(self, title, year, rating, poster, imdb_link, country_code, notes=None):
        """
        Add a new movie to the JSON file.
        Load existing movies and then save updated movie list to JSON.
        """
        movies = self._read_storage()
        movie_data = {
            'year': year,
            'rating': rating,
            'poster': poster,
            'imdb_link': imdb_link,
            'country_code': country_code,
        }
        if notes:
            movie_data['notes'] = notes
        movies[title] = movie_data
        self._write_storage(movies)

    def delete_movie(self, title):
        """
        Delete a movie from the JSON file by its title.
        """
        movies = self._read_storage()  # load existing movies

        if title in movies:
            del movies[title]
            self._write_storage(movies)

        else:
            print(f"Movie with title '{title}' not found in storage.")

    def update_movie(self, title, rating, notes=None):
        """
        Update the rating of an existing movie in the JSON file.
        """
        movies = self._read_storage()

        if title in movies:
            movies[title]['rating'] = rating

            if notes is not None:
                movies[title]['notes'] = notes
            self._write_storage(movies)

        else:
            print(f"Movie with title '{title}' not found in storage.")
