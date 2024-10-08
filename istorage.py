from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Abstract base class for movie storage.

    Any class that implements this interface should provide implementations for listing,
    adding, deleting, and updating movies in the storage.
    """

    @abstractmethod
    def list_movies(self):
        """
        Abstract method to retrieve the list of movies.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster, imdb_link, country_code, notes=None):
        """
        Abstract method to add a new movie.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Abstract method to delete a movie from the storage by its title.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating, notes=None):
        """
        Abstract method to update the rating of an existing movie in the storage.
        """
        pass
