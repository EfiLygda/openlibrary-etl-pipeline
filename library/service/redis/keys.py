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
    - reservations:active:ids (SET) - runtime reservation ids that are active
    - reservations:fulfilled:ids (SET) - runtime reservation ids that are fulfilled
    - reservations:canceled:ids (SET) - runtime reservation ids that are canceled

* Maximum Allowable Values
    - max:users (INT) - max users to register
    - max:librarians (INT) - max librarians to hire
    - hash:max:edition:copies (HASH)
        - field: edition_key
        - value: max copies allowed for current edition_key

* Runtime Counters
    - counter:users (INCR) - counting current registered users
    - counter:librarians (INCR) - counting current hired librarians
    - hash:counter:edition:copies (HASH)
        - field: edition_key
        - value: counting current edition's copies purchased
    - counter:loans (INCR) - counting all borrowings of all copies
    - counter:returns (INCR) - counting all returned loans
    - counter:renewals (INCR) - counting all loan renewals
    - counter:reservations (INCR) - counting all created reservations
    - counter:reservations:canceled (INCR) - counting all canceled reservations
"""

class RedisKeys:

    class Strings:
        MAX_USERS = 'max:users'
        MAX_LIBRARIANS = 'max:librarians'

    class Sets:
        EDITION_KEYS = 'editions:keys'

        USER_IDS = 'users:ids'
        LIBRARIAN_IDS = 'librarians:ids'

        AVAILABLE_COPIES_IDS = 'copies:available:ids'
        UNAVAILABLE_COPIES_IDS = 'copies:unavailable:ids'

        ACTIVE_LOANS_IDS = 'loans:active:ids'
        RETURNED_LOANS_IDS = 'loans:returned:ids'

        ACTIVE_RESERVATIONS_IDS = 'reservations:active:ids'
        FULFILLED_RESERVATIONS_IDS = 'reservations:fulfilled:ids'
        CANCELLED_RESERVATIONS_IDS = 'reservations:canceled:ids'
        # EXPIRED_RESERVATIONS_IDS = 'reservations:active:ids'

        UNPAID_FINES_IDS = 'fines:unpaid:ids'
        PAID_FINES_IDS = 'fines:paid:ids'

    class Counters:
        USERS = 'counter:users'
        LIBRARIANS = 'counter:librarians'
        LOANS = 'counter:loans'
        RETURNS = 'counter:returns'
        RENEWALS = 'counter:renewals'
        RESERVATIONS = 'counter:reservations'
        CANCELLED_RESERVATIONS = 'counter:reservations:canceled'
        ISSUED_FINES = 'counter:fines:unpaid'
        PAID_FINES = 'counter:fines:paid'

    class Hashes:

        MAX_EDITION_COPIES = 'max:edition:copies'
        COUNTER_EDITION_COPIES = 'counter:edition:copies'

        @staticmethod
        def loan(loan_id: str) -> str:
            return f'loan:{loan_id}'

        @staticmethod
        def reservation(reservation_id: str) -> str:
            return f'reservation:{reservation_id}'

    class Queues:

        @staticmethod
        def reservation_queue(copy_id: str) -> str:
            return f'reservations:queue:{copy_id}'