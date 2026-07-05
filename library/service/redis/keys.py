"""
Redis keys as used for the library

Redis naming conventions:
* Global IDs' Pools
    - editions:keys (SET) - all edition keys available in the database
    - users:ids (SET) - runtime user ids
    - librarians:ids (SET) - runtime librarian ids
    - copies:available:ids (SET) - runtime copy ids that are available to borrow
    - copies:unavailable:ids (SET) - runtime copy ids that are not available to borrow
    - loans:active:ids (SET) - runtime loan ids that are active
    - loans:returned:ids (SET) - runtime loan ids with returned copies

* Maximum Allowable Values
    - max:users (INT) - max users to register
    - max:librarians (INT) - max librarians to hire
    - max:edition:{edition_key}:copies (INT) - max copies for current edition_key

* Runtime Counters
    - counter:users (INCR) - counting current registered users
    - counter:librarians (INCR) - counting current hired librarians
    - counter:edition:{edition_key}:copies (INCR) - counting current edition's copies purchased
    - counter:loans (INCR) - counting all borrowings of all copies
"""

class RedisKeys:
    
    class Sets:
        EDITION_KEYS = 'editions:keys'
        USER_IDS = 'users:ids'
        LIBRARIAN_IDS = 'librarians:ids'
        AVAILABLE_COPIES_IDS = 'copies:available:ids'
        UNAVAILABLE_COPIES_IDS = 'copies:unavailable:ids'
        ACTIVE_LOANS_IDS = 'loans:active:ids'
        RETURNED_LOANS_IDS = 'loans:returned:ids'

    class MaxAllowableValues:
        USERS = 'max:users'
        LIBRARIANS = 'max:librarians'

        @staticmethod
        def edition_copies(edition_key: str) -> str:
            return f'max:edition:{edition_key}:copies'

    class Counters:
        USERS = 'counter:users'
        LIBRARIANS = 'counter:librarians'
        LOANS = 'counter:loans'

        @staticmethod
        def edition_copies(edition_key: str) -> str:
            return f'counter:edition:{edition_key}:copies'