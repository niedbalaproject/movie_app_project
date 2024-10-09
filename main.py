from movie_app_project.storage_json import StorageJson
from movie_app_project.storage_csv import StorageCsv
from movie_app_project.movie_app import MovieApp
import os
import argparse


def main():
    """
    The main function initializes the storage and the movie application,
    then runs the application.
    """

    parser = argparse.ArgumentParser(description="Movie App")
    parser.add_argument('storage_file', type=str, help='Path to the storage file (JSON or CSV.')

    # parse the arguments
    args = parser.parse_args()
    storage_file = args.storage_file.strip()

    if storage_file.endswith('.json'):
        storage = StorageJson(storage_file)
    elif storage_file.endswith('.csv'):
        storage = StorageCsv(storage_file)
    else:
        print("Invalid file type. Please provide a .json or .csv file.")
        return

    if not os.path.exists(storage_file):
        print(f"Storage file '{storage_file} does not exist.")
        return

    # Create a MovieApp object with the chosen storage type
    movie_app = MovieApp(storage)

    # Run the app
    movie_app.run()


if __name__ == "__main__":
    main()
