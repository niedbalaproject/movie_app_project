from movie_app_project.storage_json import StorageJson
from movie_app_project.storage_csv import StorageCsv  # Import the CSV storage class
from movie_app_project.movie_app import MovieApp


def main():
    """
    The main function initializes the storage and the movie application,
    then runs the application.
    """

    # Ask the user whether they want to use JSON or CSV storage
    storage_type = input("Which storage type would you like to use? (json/csv): ").strip().lower()

    if storage_type == 'json':
        # Create a StorageJson object
        storage = StorageJson('../movies.json')
    elif storage_type == 'csv':
        # Create a StorageCsv object
        storage = StorageCsv('movies.csv')  # CSV storage
    else:
        print("Invalid storage type. Please enter 'json' or 'csv'.")
        return

    # Create a MovieApp object with the chosen storage type
    movie_app = MovieApp(storage)

    # Run the app
    movie_app.run()


if __name__ == "__main__":
    main()
