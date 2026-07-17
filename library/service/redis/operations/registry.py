"""
Provides access to grouped Redis state operation handlers.
"""

import json

from library.utils.dates import add_days_to_str_date

from library.service.redis.client import RedisClient
from library.service.redis.keys import RedisKeys
from library.service.redis.operations.base import RedisOperationsBase


class _Users(RedisOperationsBase):
    """
    Provides Redis operations related to library users
    """

    def register_user(self, user_id: str) -> None:
        """
        Registers a new user in Redis state.

        Adds the user ID to the collection of known users.

        :param user_id: str, the ID of the registered user

        :return: None
        """

        self.client.sets.add(
            RedisKeys.Sets.USER_IDS,
            user_id,
        )

class _Librarians(RedisOperationsBase):
    """
    Provides Redis operations related to librarians
    """

    def register_librarian(self, librarian_id: str) -> None:
        """
        Registers a new librarian in Redis state.

        Adds the librarian ID to the collection of known librarians.

        :param librarian_id: str, the ID of the hired librarian

        :return: None
        """

        self.client.sets.add(
            RedisKeys.Sets.LIBRARIAN_IDS,
            librarian_id,
        )

class _Copies(RedisOperationsBase):
    """
    Provides Redis operations related to book copies
    """

    def register_copy(self, copy_id: str) -> None:
        """
        Registers a newly purchased copy.

        Adds the copy ID to available copies.

        :param copy_id: str, the ID of the purchased copy

        :return: None
        """

        self.client.sets.add(
            RedisKeys.Sets.AVAILABLE_COPIES_IDS,
            copy_id,
        )

    def borrow_copy(self, copy_id: str) -> None:
        """
        Marks a copy as borrowed.

        Moves a copy from available copies to unavailable copies.

        :param copy_id: str, the borrowed copy ID

        :return: None
        """

        self.client.sets.move(
            source=RedisKeys.Sets.AVAILABLE_COPIES_IDS,
            destination=RedisKeys.Sets.UNAVAILABLE_COPIES_IDS,
            value=copy_id,
        )

    def return_copy(self, copy_id: str) -> None:
        """
        Marks a copy as returned.

        Moves a copy from unavailable copies to available copies.

        :param copy_id: str, the returned copy ID

        :return: None
        """

        self.client.sets.move(
            source=RedisKeys.Sets.UNAVAILABLE_COPIES_IDS,
            destination=RedisKeys.Sets.AVAILABLE_COPIES_IDS,
            value=copy_id,
        )

    def has_copy_reservations(self, copy_id: str) -> bool:
        """
        Checks whether a copy has pending reservations.

        :param copy_id: str, the copy ID to check

        :return: bool, whether reservations exist
        """

        return self.client.queues.get_length(
                RedisKeys.Queues.reservation_queue(copy_id)
            ) > 0

class _Loans(RedisOperationsBase):
    """
    Provides Redis operations related to book loans
    """

    def create_active_loan(
            self,
            loan_id: str,
            copy_id: str,
            due_date: str,
    ) -> None:
        """
        Creates Redis state for an active loan.

        Adds the loan ID to active loans and stores loan metadata.

        :param loan_id: str, the created loan ID
        :param copy_id: str, the borrowed copy ID
        :param due_date: str, the loan due date

        :return: None
        """

        # Add new ID to Redis set to be used later
        self.client.sets.add(
            RedisKeys.Sets.ACTIVE_LOANS_IDS,
            loan_id,
        )

        # Setting up loan's hash
        self.client.hashes.set_mapping(
            RedisKeys.Hashes.loan(loan_id),
            mapping={
                "copy_id": copy_id,
                "due_date": due_date,
            },
        )

    def get_copy_id(self, loan_id: str) -> str:
        """
        Retrieves the copy ID belonging to a loan.

        :param loan_id: str, the loan ID

        :return: str, the copy ID
        """

        return str(
            self.client.hashes.get(
                name=RedisKeys.Hashes.loan(loan_id),
                key="copy_id",
            )
        )

    def get_due_date(self, loan_id: str) -> str:
        """
        Retrieves the due date belonging to a loan.

        :param loan_id: str, the loan ID

        :return: str, the due date
        """

        return str(
            self.client.hashes.get(
                name=RedisKeys.Hashes.loan(loan_id),
                key="due_date",
            )
        )

    def renew_loan(
            self,
            loan_id: str,
            days: int = 7,
    ) -> str:
        """
        Updates the due date of an active loan.

        :param loan_id: str, the loan ID
        :param days: int, days to add to original due date to calculate new due date

        :return: str, the new due date
        """

        # Fetch current due date for the loan
        current_due_date = str(
            self.client.hashes.get(
                name=RedisKeys.Hashes.loan(loan_id),
                key='due_date',
            )
        )

        # Calculate new due date after renewal
        new_due_date = add_days_to_str_date(
            date=current_due_date,
            days=days,
        )

        # Change due date to the new one in the loans hash
        self.client.hashes.set(
            name=RedisKeys.Hashes.loan(loan_id),
            key='due_date',
            value=new_due_date,
        )

        return new_due_date

    def return_loan(self, loan_id: str) -> None:
        """
        Marks a loan as returned.

        Moves loan from active loans to returned loans.

        :param loan_id: str, the loan ID

        :return: None
        """

        self.client.sets.move(
            source=RedisKeys.Sets.ACTIVE_LOANS_IDS,
            destination=RedisKeys.Sets.RETURNED_LOANS_IDS,
            value=loan_id,
        )

class _Reservations(RedisOperationsBase):
    """
    Provides Redis operations related to copy reservations
    """

    def create_reservation(
            self,
            reservation_id: str,
            copy_id: str,
            user_id: str,
    ) -> None:
        """
        Creates a new active reservation.

        Stores reservation metadata and places it in the copy queue.

        :param reservation_id: str, the reservation ID
        :param copy_id: str, the reserved copy ID
        :param user_id: str, the reserving user ID

        :return: None
        """

        # Add reservation ID to active reservations set
        self.client.sets.add(
            RedisKeys.Sets.ACTIVE_RESERVATIONS_IDS,
            reservation_id,
        )

        # Add the reservation data to the copy's reservation queue
        self.client.queues.add(
            RedisKeys.Queues.reservation_queue(copy_id),
            json.dumps({
                "reservation_id": reservation_id,
                "user_id": user_id,
            }),
        )

        # Add new reservation hash with the data
        self.client.hashes.set_mapping(
            RedisKeys.Hashes.reservation(reservation_id),
            mapping={
                "copy_id": copy_id,
                "user_id": user_id,
            },
        )

    def get_copy_id(self, reservation_id: str) -> str:
        """
        Retrieves the copy ID belonging to a reservation.

        :param reservation_id: str, reservation ID

        :return: str, copy ID
        """

        return str(
            self.client.hashes.get(
                name=RedisKeys.Hashes.reservation(reservation_id),
                key="copy_id",
            )
        )

    def get_user_id(self, reservation_id: str) -> str:
        """
        Retrieves the user ID belonging to a reservation.

        :param reservation_id: str, reservation ID

        :return: str, user ID
        """

        return str(
            self.client.hashes.get(
                name=RedisKeys.Hashes.reservation(reservation_id),
                key="user_id",
            )
        )

    def pop_next(self, copy_id: str) -> str:
        """
        Retrieves the next reservation waiting for a copy.

        :param copy_id: str, copy ID

        :return: str, serialized reservation data
        """

        return self.client.queues.pop(
            name=RedisKeys.Queues.reservation_queue(copy_id),
        )

    def cancel(self, reservation_id: str) -> tuple[str, str]:
        """
        Cancels an active reservation.

        :param reservation_id: str, reservation ID

        :return: tuple[str, str], copy ID and user ID
        """

        # Fetch the reservation's copy and user IDs
        copy_id = self.get_copy_id(reservation_id)
        user_id = self.get_user_id(reservation_id)

        # Move reservation ID from active reservations sets
        # to cancelled
        self.client.sets.move(
            source=RedisKeys.Sets.ACTIVE_RESERVATIONS_IDS,
            destination=RedisKeys.Sets.CANCELLED_RESERVATIONS_IDS,
            value=reservation_id,
        )

        # Remove the canceled reservation data from the copy's
        # reservation queue, wherever it was located
        self.client.queues.remove(
            name=RedisKeys.Queues.reservation_queue(copy_id),
            value=json.dumps({
                "reservation_id": reservation_id,
                "user_id": user_id,
            }),
        )

        return copy_id, user_id

    def fulfill(self, reservation_id: str) -> None:
        """
        Marks a reservation as fulfilled.

        :param reservation_id: str, reservation ID

        :return: None
        """

        self.client.sets.move(
            source=RedisKeys.Sets.ACTIVE_RESERVATIONS_IDS,
            destination=RedisKeys.Sets.FULFILLED_RESERVATIONS_IDS,
            value=reservation_id,
        )

class _Fines(RedisOperationsBase):
    """
    Provides Redis operations related to fines
    """

    def issue(self, fine_id: str) -> None:
        """
        Marks a fine as unpaid.

        Stores the fine ID in the unpaid fines set to track fines
        that require payment.

        :param fine_id: str, the fine ID

        :return: None
        """

        # Add new ID to Redis set to be used later
        self.client.sets.add(
            RedisKeys.Sets.UNPAID_FINES_IDS,
            fine_id,
        )

    def pay(self, fine_id: str) -> None:
        """
        Marks a fine as paid.

        Moves a fine from unpaid fines to paid fines.

        :param fine_id: str, the fine ID

        :return: None
        """

        # Add new ID to Redis set to be used later
        self.client.sets.move(
            RedisKeys.Sets.UNPAID_FINES_IDS,
            RedisKeys.Sets.PAID_FINES_IDS,
            fine_id,
        )

class RedisOperations:
    """
    Aggregates Redis operations by library domain
    """

    def __init__(self, redis_client: RedisClient):

        self.client = redis_client

        self.users = _Users(redis_client)
        self.librarians = _Librarians(redis_client)
        self.copies = _Copies(redis_client)
        self.loans = _Loans(redis_client)
        self.reservations = _Reservations(redis_client)
        self.fines = _Fines(redis_client)
