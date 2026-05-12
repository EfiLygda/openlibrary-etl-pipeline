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
    WORK_ID_PATTERN = r'OL\d+W'
    AUTHOR_ID_PATTERN = r'OL\d+A'
    BOOK_ID_PATTERN = r'OL\d+M'
    SERIES_ID_PATTERN = r'OL\d+L'

    @staticmethod
    def detect_key(key: str) -> str | None:

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
        return json.dumps(lst)
