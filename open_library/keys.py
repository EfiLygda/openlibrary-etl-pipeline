import re
import json

class KeyHandler:
    # Normalized Open Library keys prefixes
    KEYS_NORMALIZED_PREFIXES = [
        "/authors/",
        "/works/",
        "/books/",
        "/series/",
        "/subjects/time:",
        "/subjects/person:",
        "/subjects/",
        "/publishers/"
    ]

    # Basic Open Library IDs regex
    key_patterns = {
        'work': r'OL\d+W',
        'author': r'OL\d+A',
        'edition': r'OL\d+M',
        'series': r'OL\d+L'
    }

    @staticmethod
    def detect_key(key: str) -> str | None:
        """
        Function for detecting the type of Open Library key.
        :param key: str, the string that contains the key
        :return: str, returns one between these values ["author", "work", "series", "edition",
                      "subject_time", "subject_person", "subject", "publisher"] or None if the type
                      cannot be detected
        """
        if not key.startswith('/') and not key.startswith('OL'):
            key = '/' + key

        if key.startswith("/authors/") or (key.startswith("OL") and key.endswith("A")):
            return "author"
        elif key.startswith("/works/") or (key.startswith("OL") and key.endswith("W")):
            return "work"
        elif key.startswith("/series/") or (key.startswith("OL") and key.endswith("L")):
            return "series"
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
        """
        Function for normalizing a key by adding the right prefix
        :param key: str, the string containing the key
        :return: str, the normalized key
        """
        if (key.startswith("OL") or key.startswith("author:OL")) and key.endswith("A"):
            return f"/authors/{key.replace('author:', '')}"
        elif (key.startswith("OL") or key.startswith("work:OL")) and key.endswith("W"):
            return f"/works/{key.replace('work:', '')}"
        elif (key.startswith("OL") or key.startswith("series:OL")) and key.endswith("L"):
            return f"/series/{key.replace('series:', '')}"
        elif (key.startswith("OL") or key.startswith("book:OL")) and key.endswith("M"):
            return f"/books/{key.replace('book:', '')}"
        elif key.startswith("publisher:"):
            return f"/publishers/{key.replace('publisher:', '')}"
        elif key.startswith("subject:"):
            return f"/subjects/{key.replace('subject:', '')}"
        elif key.startswith("time:"):
            return f"/subjects/{key}"
        elif key.startswith("person:"):
            return f"/subjects/{key}"

        else:
            if not key.startswith('/'):
                return '/' + key
            else:
                return key

    @staticmethod
    def key_list_2_str(lst: list[str]) -> str:
        """
        Function for converting a list of keys to string representation of the list
        :param lst: lst[str], list containing the keys
        :return: str, string representation of the list
        """
        return json.dumps(lst)

    @staticmethod
    def get_key(text: str, mode: str = '') -> str | None:
        """
        Function for extracting the key from a string
        :param text: str, the string that contains the key
        :param mode: str, the type of key given. Value must be in ['work','author','book','series']
        :return: str | None, the key denormalized or None if it is not found
        """

        # If the mode is not given then there will be an attempt to detect it
        # If it is not detected then the key will not be found and None if it is not found
        if not mode:
            mode = KeyHandler.detect_key(text)
        else:
            return None

        # If the mode is not in the predetermined values then a ValueError is raised
        if mode not in KeyHandler.key_patterns.keys():
            raise ValueError(
                f'Value \'{mode}\' for argument \'mode\' not valid. Use \'work\', \'author\', \'book\' or \'series\'.'
            )

        # Find all matches for the key
        # It is noted what for this function the text is expected to only return one match
        matches = re.findall(KeyHandler.key_patterns[mode], text)

        # Checking if there are matches for the key pattern
        if matches:

            # If more than one match is found then the text is invalid and a ValueError is returned
            if len(matches) > 1:
                raise ValueError(f'\'text\': {text} contains more than one keys')

            # Else the right match - key is returned
            return matches[0]

        else:
            # If no matches were found then None is returned
            return None