import requests

from open_library import JSONFileHandler, KeyHandler

class Client:

    # Base urls for Open Library API
    BASE_URL = 'https://openlibrary.org'

    def __init__(self):
        self.session = requests.Session()

        # Limiting to 100 records per page
        self.LIMIT = 100

        # Setting the connection and reading timeouts
        self.CONNECT_TIMEOUT = 15
        self.READ_TIMEOUT = 15

        # Current successful query
        self.last_url = ''

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

        # try:
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

        # except requests.exceptions.RequestException as e:
        #     # Print error message and return None
        #     print(f"Request failed: {e}")
        #     return None
    # -----------------------------------------------------------------------------------


    # -----------------------------------------------------------------------------------
    # --- Fetch Methods ---
    def search(
            self,
            query: str = '',
            mode: str = 'works',
            **kwargs
    ) -> dict | None :
        """
        Function for quering Open Library API to retrieve book data or author's enriched data
        :param query: str, the query used for the API
        :param mode: str, the mode used for querying the API, 'works' returns general works data, 'authors' enriched data
        :param kwargs:  dict, dictionary containing additional parameters for the query (Read more: https://openlibrary.org/dev/docs/api/search)
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Set up the parameters for the query
        request_params = {'limit': self.LIMIT}

        # Setting the base url for searching the API
        if mode == 'works':
            search_base_url = f'{self.BASE_URL}/search.json'
        elif mode == 'authors':
            search_base_url = f'{self.BASE_URL}/search/authors.json'
        else:
            raise ValueError(f'\'mode\' argument must be either \'works\' or \'authors\'')

        # Setting up the query used, if it is passed
        if query:
            request_params['q'] = query

        # Add the new parameters as passed
        request_params.update(kwargs)

        # Request and return the JSON response
        return self.request(search_base_url, request_params)

    def get_author(self, author_key: str) -> dict | None :
        """
        Function for quering Open Library API to retrieve author data
        :param author_key: str, OLxxxxA like string of an authors key
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Setting the base url for searching the API
        author_url = f'{self.BASE_URL}/authors/{author_key}.json'

        # Request and return the JSON response
        return self.request(author_url)

    def get_series(
            self,
            series_key: str,
            works: bool = False
    ) -> dict | None :
        """
        Function for quering Open Library API to retrieve series data
        :param series_key: str, OLxxxxL like string of a series key
        :param works: book, if True all general works that are in the series are returned
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Setting the base url for searching the API
        if works:
            series_url = f'{self.BASE_URL}/series/{series_key}/seeds.json'
        else:
            series_url = f'{self.BASE_URL}/series/{series_key}.json'

        # Request and return the JSON response
        return self.request(series_url)

    def get_work(
            self,
            work_key: str,
            editions: bool = False,
            **kwargs
    ) -> dict | None :
        """
        Function for quering Open Library API to retrieve book data
        :param work_key: str, OLxxxxW like string of a work's key
        :param editions: bool, whether to return all editions related to the work
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Setting the base url for searching the API
        if editions:
            work_url = f'{self.BASE_URL}/works/{work_key}/editions.json'
        else:
            work_url = f'{self.BASE_URL}/works/{work_key}.json'

        # Request and return the JSON response
        return self.request(work_url, kwargs)

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

    def get_publisher(self, publisher: str, **kwargs) -> dict | None :
        """
        Function for quering Open Library API to retrieve publisher data
        :param publisher: str, publisher name
        :param kwargs: additional arguments for query
        :return: dict | None, returns JSON response or None in case there was an error
        """
        # Setting the base url for searching the API
        publisher_url = f'{self.BASE_URL}/publishers/{publisher}.json'

        # Request and return the JSON response
        return self.request(publisher_url, kwargs)

    def get_subject(
            self,
            subject: str,
            subject_type: str | None = None,
            **kwargs
    ) -> dict | None :
        """
        Function for quering Open Library API to retrieve subject data
        :param subject: str, subject name
        :param subject_type: str | None, must be either 'time' or 'person', else an ValueError raised
        :param kwargs: additional arguments for query
        :return: dict | None, returns JSON response or None in case there was an error
        """
        # Setting the base url for searching the API
        if not subject_type:
            subject_url = f'{self.BASE_URL}/subjects/{subject}.json'
        elif subject_type.lower() in ['time', 'person']:
            subject_url = f'{self.BASE_URL}/subjects/{subject_type.lower()}:{subject}.json'
        else:
            raise ValueError(f'\'subject_type\' argument must be either \'time\' or \'person\'')

        # Request and return the JSON response
        return self.request(subject_url, kwargs)

    def get(self, key: str, **kwargs) -> dict | None :
        """
        Function for quering Open Library API to retrieve a records data
        :param key: str, string of a record's key.
                         Must be valid Open Library key:
                         1. Work:       'OLxxxxW', 'work:{OLxxxxW}', '/works/OLxxxxW' or 'works/OLxxxxW'
                         2. Author:     'OLxxxxA', 'author:{OLxxxxA}', '/authors/OLxxxxA' or 'authors/OLxxxxA'
                         3. Edition:    'OLxxxxM', 'book:{OLxxxxM}', '/books/OLxxxxM' or 'books/OLxxxxM'
                         4. Subject:    subject:{name_of_subject}
                         5. Person:     person:{name_of_person}
                         6. Time:       time:{time_period_name}
        :return: dict | None, returns JSON response or None in case there was an error
        """

        # Setting the base url for searching the API
        url = f'{self.BASE_URL}{KeyHandler.normalize_key(key)}.json'

        # Request and return the JSON response
        return self.request(url, **kwargs)

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
        normalized_key_list = [KeyHandler.normalize_key(k) for k in key_list]

        # Set up the parameters for the query
        request_params = {'keys': KeyHandler.key_list_2_str(normalized_key_list)}

        # Request and return the JSON response
        return self.request(get_many_url, request_params)
    # -----------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------
    @staticmethod
    def is_redirect(record: dict) -> bool:
        """
        Function for checking if a record redirects, USED only for one record responses
        like in WORKS, AUTHORS and BOOKS
        :param record: dict, a record (NOT a response)
        :return: book, True is it redirects, False if it is the original record
        """
        return 'redirect' in record['type']['key']

    def get_redirected_record(self, record: dict) -> dict | None:
        """
        Function for getting the original record from a redirect, USED only for one record responses
        like in WORKS, AUTHORS and BOOKS
        :param record: : dict, a record (NOT a response)
        :return: dict, the record that redirects to, or None if it doesn't redirect anywhere
        """
        if self.is_redirect(record):
            redirect_key = record['location'] # The key that it redirects to
            return self.get(redirect_key)
        else:
            return None
    # -----------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------
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
        JSONFileHandler.save_json(data, filename)

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
        JSONFileHandler.save_json(data, filename)
    # -----------------------------------------------------------------------------------