"""
Contains client class for querying Open Library API
"""
import json
import requests

class OpenLibraryClient:

    def __init__(self):
        self.session = requests.Session()

        # Base urls for Open Library API
        self.BASE_URL = 'https://openlibrary.org'

        # Limiting to 100 records per page
        self.LIMIT = 100

        # Setting the connection and reading timeouts
        self.CONNECT_TIMEOUT = 15
        self.READ_TIMEOUT = 15

        # Current query
        self.last_url = ''

    @staticmethod
    def normalize_key(key: str) -> str:

        # ------------------------------------------------------------------------
        # --- Open Library API - IDs small explanation ---
        # Work ID    -> OLxxxxW (the abstract work, e.g. Pride and Prejudice)
        # Edition ID -> OLxxxxM (specific edition)
        # Author ID  -> OLxxxxA (specific author)
        # -----------------------------------------------------------------------

        if key.startswith("OL") and key.endswith("A"):
            return f"/authors/{key}"
        elif key.startswith("OL") and key.endswith("W"):
            return f"/works/{key}"
        elif key.startswith("OL") and key.endswith("M"):
            return f"/books/{key}"
        else:
            return key

    @staticmethod
    def key_list_2_str(lst: list[str]):
        return json.dumps(lst)

    def request(
            self,
            url: str,
            request_params: dict | None = None
    ) -> dict | None :
        """
        Basic wrapper for requests with error handling

        :param url : str, the base url for the request
        :param request_params: dict, dictionary containing the parameters of the request
        :return: dict | None, returns JSON response or None in case there was an error
        """

        try:
            # Querying the API
            response = self.session.get(
                url,
                params=request_params,
                timeout=(self.CONNECT_TIMEOUT, self.READ_TIMEOUT)
            )

            # If the URL is invalid or returns a 4xx/5xx status code, it raises an HTTPError.
            response.raise_for_status()

            # Change the object's current url to the last requested
            self.last_url = response.url

            # Returns the JSON response as a dictionary
            return response.json()

        except requests.exceptions.RequestException as e:
            # Print error message and return None
            print(f"Request failed: {e}")
            return None

    def search(self, **kwargs) -> dict | None :
        """
        Function for quering Open Library API to retrieve book data
        :param kwargs:  dict, dictionary containing additional parameters for the query (Read more: https://openlibrary.org/dev/docs/api/search)
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Setting the base url for searching the API
        SEARCH_BASE_URL = f'{self.BASE_URL}/search.json'

        # Set up the parameters for the query
        request_params = {'limit': self.LIMIT}

        # Add the new parameters as passed
        request_params.update(kwargs)

        # Request and return the JSON response
        return self.request(SEARCH_BASE_URL, request_params)

    def get_author(self, author_key: str) -> dict | None :
        """
        Function for quering Open Library API to retrieve book data
        :param author_key: str, OLxxxxA like string of an authors key
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Setting the base url for searching the API
        author_url = f'{self.BASE_URL}/authors/{author_key}.json'

        # Request and return the JSON response
        return self.request(author_url)

    def get_work(self, work_key: str) -> dict | None :
        """
        Function for quering Open Library API to retrieve book data
        :param work_key: str, OLxxxxW like string of a work's key
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Setting the base url for searching the API
        work_url = f'{self.BASE_URL}/works/{work_key}.json'

        # Request and return the JSON response
        return self.request(work_url)

    def get_edition(self, edition_key: str) -> dict | None :
        """
        Function for quering Open Library API to retrieve book data
        :param edition_key: str, OLxxxxM like string of a work's key
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Setting the base url for searching the API
        edition_url = f'{self.BASE_URL}/books/{edition_key}.json'

        # Request and return the JSON response
        return self.request(edition_url)

    def get_many(self, key_list: list[str]) -> dict | None :
        """
        Function for quering Open Library API to retrieve book data
        :param key_list: list[str], list of keys for records to fetch
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Setting the base url for searching the API
        get_many_url = f'{self.BASE_URL}/api/get_many'

        # Normalize keys
        normalized_key_list = [self.normalize_key(k) for k in key_list]

        # Set up the parameters for the query
        request_params = {'keys': self.key_list_2_str(normalized_key_list)}

        # Request and return the JSON response
        return self.request(get_many_url, request_params)
