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
    parser.add_argument('storage_file', nargs='?', default='john.json',
                        help='Path to the storage file (JSON or CSV). Default is "movies.json".')

    # Parse the arguments
    args = parser.parse_args()
    storage_file = args.storage_file.strip()

    # If the storage file doesn't exist, prompt the user to create a new one
    if not os.path.exists(storage_file):
        print(f"Storage file '{storage_file}' does not exist.")

        # Ask the user if they want to create a new file
        create_new = input("Would you like to create a new file? (yes/no): ").strip().lower()
        if create_new != 'yes':
            print("Exiting without creating a new file.")
            return

        # Ask the user for a name for the new file
        new_file_name = input("Enter a name for the new file (with .json or .csv extension): ").strip()

        # Check if the user entered a valid file type
        if not (new_file_name.endswith('.json') or new_file_name.endswith('.csv')):
            print("Invalid file type. Please provide a file with a .json or .csv extension.")
            return

        # Update the storage_file variable with the new file name
        storage_file = new_file_name

    # Initialize the storage based on the file extension
    if storage_file.endswith('.json'):
        storage = StorageJson(storage_file)
    elif storage_file.endswith('.csv'):
        storage = StorageCsv(storage_file)
    else:
        print("Invalid file type. Please provide a .json or .csv file.")
        return

    # If the file still doesn't exist (new file), create it
    if not os.path.exists(storage_file):
        print(f"Creating a new file: '{storage_file}'.")

        # Initialize an empty library for the new user by adding a placeholder movie
        storage.add_movie(
            title="Sample Movie",
            year="2024",
            rating=0.0,
            poster="https://example.com/poster.jpg",
            imdb_link="https://www.imdb.com/title/tt0000001/",
            country_code="US",
            notes="This is a sample movie entry."
        )
        print(f"Initialized new storage with a sample movie in '{storage_file}'.")

    # Create a MovieApp object with the chosen storage type
    movie_app = MovieApp(storage)

    # Run the app
    movie_app.run()


if __name__ == "__main__":
    main()
