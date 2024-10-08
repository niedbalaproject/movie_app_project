import csv
import os
from movie_app_project.istorage import IStorage


class StorageCsv(IStorage):
    """
    IStorage interface implementation for storing movie data in a CSV file.
    """

    def __init__(self, file_path):
        """
        Initialize the StorageCsv instance.

        Args:
            file_path (str): The path to the CSV file.
        """
        self.file_path = file_path
        # Create the file if it doesn't exist with the correct header
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["title", "rating", "year", "poster", "imdb_link", "country_code", "notes"])

    def _read_storage(self):
        """Reads the CSV storage file and returns the data as a dictionary."""
        movies = {}
        try:
            with open(self.file_path, "r", newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                # Print the fieldnames for debugging
                print("Fieldnames:", reader.fieldnames)  # Check the field names

                for row in reader:
                    # Ensure that row is indeed a dictionary
                    if isinstance(row, dict):
                        # Print the current row for debugging
                        print("Row data:", row)  # Debug output
                        title = row['title']

                        movies[title] = {
                            'rating': float(row['rating']),
                            'year': row['year'],
                            'poster': row['poster'],
                            'imdb_link': row['imdb_link'],
                            'country_code': row['country_code'],
                            'notes': row.get('notes', None)  # Handle notes if they exist
                        }
                    else:
                        print("Unexpected row format:", row)  # Print if row is not a dict
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found.")
        return movies

    def _write_storage(self, data):
        """Writes the data to the CSV storage file."""
        with open(self.file_path, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["title", "rating", "year", "poster", "imdb_link", "country_code", "notes"])  # Write header
            for title, details in data.items():
                writer.writerow([
                    title,
                    details['rating'],
                    details['year'],
                    details['poster'],
                    details['imdb_link'],
                    details['country_code'],
                    details.get('notes', '')
                ])

    def list_movies(self):
        """List all movies from storage."""
        return self._read_storage()

    def add_movie(self, title, year, rating, poster, imdb_link, country_code, notes=None):
        """
        Add a new movie to the CSV file.
        Load existing movies and then save updated movie list to CSV.
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
        Delete a movie from the CSV file by its title.
        """
        movies = self._read_storage()  # load existing movies
        if title in movies:
            del movies[title]
            self._write_storage(movies)
        else:
            print(f"Movie with title '{title}' not found in storage.")

    def update_movie(self, title, rating, notes=None):
        """
        Update the rating of an existing movie in the CSV file.
        """
        movies = self._read_storage()
        if title in movies:
            movies[title]['rating'] = rating
            if notes is not None:
                movies[title]['notes'] = notes
            self._write_storage(movies)
        else:
            print(f"Movie with title '{title}' not found in storage.")
