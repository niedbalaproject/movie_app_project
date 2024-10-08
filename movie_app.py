import requests
import os
import pycountry


class MovieApp:
    """
    The MovieApp class manages movies, interacts with a storage backend,
    and provides menu-based interaction for users.
    """

    API_KEY = "e88a7016"
    BASE_URL = f"http://www.omdbapi.com/?apikey={API_KEY}&"

    def __init__(self, storage):
        """
        Initialize the MovieApp with a given storage backend.

        Args:
            storage (IStorage): A storage backend that implements the IStorage interface.
        """
        self._storage = storage

    @staticmethod
    def _get_country_code(country_name):
        """Fetch the country code for the given country name."""
        try:
            country = pycountry.countries.lookup(country_name.strip())
            return country.alpha_2 if hasattr(country, 'alpha_2') else None
        except (LookupError, AttributeError) as e:
            print(f"Country code for '{country_name}' not found: {e}.")
        return None

    def _fetch_movie_data(self, title):
        """Fetch movie data from the OMDb API."""
        try:
            response = requests.get(self.BASE_URL + f"t={title}")
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == "True":
                    try:
                        rating = float(data.get("imdbRating", 0.0))
                    except ValueError:
                        rating = 0.0
                    imdb_link = f"https://www.imdb.com/title/{data.get('imdbID', 'N/A')}/"
                    country_code = self._get_country_code(data.get("Country", "").split(",")[0]) if data.get(
                        "Country") else None
                    return {
                        "title": data.get("Title", "N/A"),
                        "year": data.get("Year", "N/A"),
                        "rating": rating,
                        "poster": data.get("Poster", ""),
                        "imdb_link": imdb_link,
                        "country_code": country_code
                    }
                else:
                    print(f"Movie '{title}' not found!")
            else:
                print(f"Failed to fetch data from OMDb API. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from OMDb API: {e}")
        return None

    def _command_list_movies(self):
        """List all movies stored in the app."""
        movies = self._storage.list_movies()
        print(f"{len(movies)} movies in total\n")
        for title, details in movies.items():
            note = details.get('notes')  # Get the note if available
            if note:
                print(f"{title} ({details['year']}): {details['rating']} - Note: {note}")
            else:
                print(f"{title} ({details['year']}): {details['rating']}")

    def _command_movie_stats(self):
        """Display various movie statistics like average, median, best and worst movies."""
        movies = self._storage.list_movies()

        if not movies:
            print("No movies in the storage.")
            return

        ratings = [details['rating'] for details in movies.values()]
        average_rating = sum(ratings) / len(ratings)
        median_rating = sorted(ratings)[len(ratings) // 2] if len(ratings) % 2 == 1 else \
            (sorted(ratings)[len(ratings) // 2 - 1] + sorted(ratings)[len(ratings) // 2]) / 2

        best_movie = max(movies.items(), key=lambda x: x[1]['rating'])
        worst_movie = min(movies.items(), key=lambda x: x[1]['rating'])

        print(f"Average rating: {average_rating:.2f}")
        print(f"Median rating: {median_rating:.2f}")
        print(f"Best movie: {best_movie[0]} ({best_movie[1]['year']}), Rating: {best_movie[1]['rating']}")
        print(f"Worst movie: {worst_movie[0]} ({worst_movie[1]['year']}), Rating: {worst_movie[1]['rating']}")

    def _command_add_movie(self):
        """Add a new movie to the storage."""
        title = input("Enter the movie title: ")
        movies = self._storage.list_movies()

        if title in movies:
            print(f"Movie '{title}' already exists!")
            return

        movie_data = self._fetch_movie_data(title)
        if movie_data:
            self._storage.add_movie(
                title=movie_data['title'],
                year=movie_data['year'],
                rating=movie_data['rating'],
                poster=movie_data['poster'],
                imdb_link=movie_data['imdb_link'],
                country_code=movie_data['country_code']
            )
            print(f"Movie '{title}' added successfully.")

    def _command_delete_movie(self):
        """Delete a movie from the storage."""
        title = input("Enter the movie title to delete: ")
        movies = self._storage.list_movies()

        if title in movies:
            self._storage.delete_movie(title)
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")

    def _command_update_movie(self):
        """Update the rating and notes for a movie."""
        title = input("Enter the movie title: ")
        movies = self._storage.list_movies()

        if title not in movies:
            print(f"Movie '{title}' not found!")
            return

        while True:
            try:
                rating = float(input("Enter the new rating (0-10): "))
                if 0 <= rating <= 10:
                    break
                else:
                    print("Please enter a rating between 0 and 10.")
            except ValueError:
                print("Invalid input, please enter a number.")

        add_note = input("Do you want to add a note? (y/n): ").lower()
        note = input("Enter the note: ") if add_note == 'y' else None
        self._storage.update_movie(title, rating, note)
        print(f"Movie '{title}' updated successfully.")

    def _command_random_movie(self):
        """Pick a random movie from the storage."""
        import random  # Used here in this specific function
        movies = self._storage.list_movies()

        if not movies:
            print("No movies available.")
            return

        title, details = random.choice(list(movies.items()))
        print(f"Random movie: {title}, Rating: {details['rating']}")

    def _command_search_movie(self):
        """Search for a movie by part of its title."""
        search_term = input("Enter part of the movie title: ").lower()
        movies = self._storage.list_movies()

        found_movies = [f"{title}, ({details['year']}), {details['rating']}" for title, details in movies.items() if
                        search_term in title.lower()]
        if found_movies:
            print("\n".join(found_movies))
        else:
            print("No matching movies found.")

    def _command_movies_sorted_by_rating(self):
        """Display all movies sorted by rating."""
        movies = self._storage.list_movies()

        sorted_movies = sorted(movies.items(), key=lambda x: (-x[1]['rating'], x[0]))
        for title, details in sorted_movies:
            print(f"{title} ({details['year']}): {details['rating']}")

    def _generate_website(self):
        """Generate an HTML page with the movie list."""
        try:
            movies = self._storage.list_movies()
            template_title = "My Movie App"
            template_movie_grid = ""

            for title, details in movies.items():
                notes = details.get('notes', '')
                imdb_link = details.get('imdb_link', '#')
                country_flag_url = f"https://flagcdn.com/32x24/{details['country_code'].lower()}.png" \
                    if details.get('country_code') else ""

                flag_img_tag = f"<img src='{country_flag_url}' alt='Country Flag' class='country-flag' />" \
                    if country_flag_url else ""

                template_movie_grid += (f"<li class='movie'>\
                    <a href='{imdb_link}' target='_blank'><img src='{details['poster']}' \
                    alt='Movie Poster' class='movie-poster'></a>\
                    <div class='movie-details'>\
                    <div class='movie-title'>{title}</div>\
                    <div class='movie-year'>{details['year']}</div>\
                    <div class='movie-rating'>Rating: {details['rating']}</div>\
                    {flag_img_tag}\
                    <div class='movie-notes'>{notes}</div>\
                    </div></li>\n")

            current_dir = os.path.dirname(os.path.abspath(__file__))
            template_file_path = os.path.join(current_dir, 'index_template.html')
            with open(template_file_path, 'r') as file:
                template_content = file.read()

            template_content = template_content.replace('__TEMPLATE_TITLE__', template_title)
            template_content = template_content.replace('__TEMPLATE_MOVIE_GRID__', template_movie_grid)

            output_file_path = os.path.join(current_dir, '../my_movie_app.html')
            with open(output_file_path, 'w') as file:
                file.write(template_content)

            print("Website generated successfully.")

        except Exception as e:
            print(f"Error generating website: {e}")

    def run(self):
        """Run the MovieApp by displaying a menu and handling user commands."""
        commands = {
            "1": ("List movies", self._command_list_movies),
            "2": ("Movie stats", self._command_movie_stats),
            "3": ("Add movie", self._command_add_movie),
            "4": ("Delete movie", self._command_delete_movie),
            "5": ("Update movie", self._command_update_movie),
            "6": ("Random movie", self._command_random_movie),
            "7": ("Search movie", self._command_search_movie),
            "8": ("Movies sorted by rating", self._command_movies_sorted_by_rating),
            "9": ("Generate website", self._generate_website),
            "0": ("Exit", lambda: print("Exiting... Thank you for using My Movie app!"))
        }

        while True:
            print("\nMovie App Menu")
            for cmd_id, (cmd_description, _) in commands.items():
                print(f"{cmd_id}. {cmd_description}")
            choice = input("\nEnter your choice: ")

            if choice == "0":
                commands[choice][1]()
                break
            elif choice in commands:
                commands[choice][1]()
            else:
                print("Invalid choice! Please try again.")
