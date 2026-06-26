"""
Service configuration registry for dynamic entity resolution

This module defines the ServiceConfig structure and the concrete configurations
used to drive generic service handlers for API endpoints
"""

from pydantic import BaseModel
from typing import TypeVar, Type, Callable, Any

T = TypeVar('T', bound=BaseModel)

class ServiceConfig:
    """
    Configuration container for entity-based service resolution

    This class defines the minimal metadata required to dynamically resolve
    batch and relationship API behavior for a given entity type.

    :param repository_function: Callable[..., dict[str, Any]], callable that retrieves data
        from the persistence layer.

        Must return a dictionary containing at minimum:
            - data
            - column_names
            - total_parents (optional)
            - total_children (optional)

        Expected parameters (may vary slightly by use case):
            - connection
            - keys or filter_key
            - limit (optional)
            - offset (optional)

    :param response_base_model: Type[T], pydantic model used to validate and serialize returned records.
        Ensures consistent API schema across dynamically resolved services
    :param router_entity_type: str, logical identifier for the router's entity domain ("work", "author",
        "edition"). Used for validation, error handling, and metadata generation
    :param endpoint_child_type: str, logical identifier for the endpoint's child domain ("work", "author",
        "edition", etc.). Used for metadata generation
    """
    def __init__(
            self,
            repository_function: Callable[..., dict[str, Any]],
            response_base_model: Type[T],
            router_entity_type: str,
            endpoint_child_type: str | None = None,
    ):
        self.router_entity_type = router_entity_type
        self.repository_function = repository_function
        self.response_base_model = response_base_model
        self.endpoint_child_type = endpoint_child_type
