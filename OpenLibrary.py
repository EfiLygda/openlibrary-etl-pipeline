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

        # Normalized Open Library keys prefixes
        self.OL_KEYS_NORMALIZED_PREFIXES = [
            "/authors/",
            "/works/",
            "/books/",
            "/subjects/time:",
            "/subjects/person:",
            "/subjects/",
            "/publishers/"
        ]

        # Current query
        self.last_url = ''

    # -----------------------------------------------------------------------------------
    # --- Helper Methods ---
    @staticmethod
    def detect_record(key: str) -> str | None:
        if key.startswith("/authors/") or (key.startswith("OL") and key.endswith("A")):
            return "author"
        elif key.startswith("/works/") or (key.startswith("OL") and key.endswith("W")):
            return "work"
        elif key.startswith("/books/") or (key.startswith("OL") and key.endswith("M")):
            return "edition"
        elif key.startswith("/subjects/time:"):
            return "subject_time"
        elif key.startswith("/subjects/person:"):
            return "subject_person"
        elif key.startswith("/subjects/"):
            return "subject"
        elif key.startswith("/publishers/"):
            return "publisher"
        return None

    @staticmethod
    def normalize_key(key: str) -> str:

        if key.startswith("OL") and key.endswith("A"):
            return f"/authors/{key}"
        elif key.startswith("OL") and key.endswith("W"):
            return f"/works/{key}"
        elif key.startswith("OL") and key.endswith("M"):
            return f"/books/{key}"
        else:
            if not key.startswith('/'):
                return '/' + key
            else:
                return key

    @staticmethod
    def key_list_2_str(lst: list[str]) -> str:
        return json.dumps(lst)
    # -----------------------------------------------------------------------------------


    # -----------------------------------------------------------------------------------
    # --- Main Request Method ---
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

            # Change the object's current url to the last requested
            self.last_url = response.url

            # If the URL is invalid or returns a 4xx/5xx status code, it raises an HTTPError.
            # None will be returned if it is raised
            response.raise_for_status()

            # Returns the JSON response as a dictionary
            return response.json()

        except requests.exceptions.RequestException as e:
            # Print error message and return None
            print(f"Request failed: {e}")
            return None
    # -----------------------------------------------------------------------------------


    # -----------------------------------------------------------------------------------
    # --- Fetch Methods ---
    def search(self, **kwargs) -> dict | None :
        """
        Function for quering Open Library API to retrieve book data
        :param kwargs:  dict, dictionary containing additional parameters for the query (Read more: https://openlibrary.org/dev/docs/api/search)
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Setting the base url for searching the API
        search_base_url = f'{self.BASE_URL}/search.json'

        # Set up the parameters for the query
        request_params = {'limit': self.LIMIT}

        # Add the new parameters as passed
        request_params.update(kwargs)

        # Request and return the JSON response
        return self.request(search_base_url, request_params)

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
        :param edition_key: str, OLxxxxM like string of an edition's key
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Setting the base url for searching the API
        edition_url = f'{self.BASE_URL}/books/{edition_key}.json'

        # Request and return the JSON response
        return self.request(edition_url)

    def get(self, key: str) -> dict | None :
        """
        Function for quering Open Library API to retrieve a records data
        :param key: str, string of a record's key
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Setting the base url for searching the API
        url = f'{self.BASE_URL}{self.normalize_key(key)}.json'

        # Request and return the JSON response
        return self.request(url)

    def get_many(
            self,
            key_list: list[str] | tuple[str, ...]
    ) -> dict | None :
        """
        Function for quering Open Library API to retrieve many records at the same time
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
    # -----------------------------------------------------------------------------------


    # -----------------------------------------------------------------------------------
    # --- Export Methods ---
    def save_json(
            self,
            data: dict | None,
            filename: str
    ) -> None:
        """
        Helper function for saving response as JSON files
        :param data: dict | None, containing the response from the API
        :param filename: str, the file name or path for saving the file
        :return: None
        """

        # In case no data was returned then a ValueError is raised
        if data is None:
            raise ValueError(f'No data was returned for query {self.last_url}')

        # Is case the another type is used for saving the data ValueError is raised
        if not filename.endswith('.json'):
            raise ValueError("File must be a JSON file")

        # Saving the data as a JSON file with pretty print (intent: 4 space)
        with open(filename, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def save(
            self,
            key: str | list[str] | tuple[str, ...],
            filename: str
    ) -> None:
        """
        Function for saving the responses of the API.
        :param key: str | list[str] | tuple[str, ...], a single or more keys can be passed for querying the API
        :param filename: str, the file name or path for saving the file
        :return: None
        """

        # If a single key was passed the 'get' method is used that automatically
        # uses thr right query
        if isinstance(key, str):
            data = self.get(key)

        # In case a list or tuple is passes the 'get_many' method is used
        elif isinstance(key, list) or isinstance(key, tuple):

            # In case not all keys are strings in the 'key' argument a ValueError is raised
            if not all(isinstance(k, str) for k in key):
                raise ValueError('\'key\' argument must be string or list/tuple of strings.')

            data = self.get_many(key)
        else:

            # In case of wrong type for 'key' argument a ValueError is raised
            raise ValueError('\'key\' argument must be string or list/tuple of strings.')

        # Save the response as a JSON file
        self.save_json(data, filename)

    def save_search(
            self,
            filename: str,
            **kwargs
    ) -> None:
        """
        Function for saving the result of a SEARCH query via the API
        :param filename: str, the file name or path for saving the file
        :param kwargs: additional arguments to be passed (More: https://openlibrary.org/dev/docs/api/search)
        :return: None
        """

        # Query the API via SEARCH
        data = self.search(**kwargs)

        # Save the response as a JSON file
        self.save_json(data, filename)
    # -----------------------------------------------------------------------------------

