"""
Meta builders for API response structures
"""

def build_entity_meta(entity_type: str) -> dict:
    """
    Build metadata for single-entity responses

    This standardizes the `meta` section for entity endpoints
    so that all entity responses consistently expose their type

    :param entity_type: str, the type of entity being returned (e.g. "work", "author")

    :return: dict, dictionary containing entity metadata
    """
    return {
        'type': entity_type
    }

def build_relationship_meta(
        parent_type: str,
        parent_key: str,
        child_type: str,
        total_children: int,
        limit: int,
        offset: int
):
    """
    Build metadata for relationship (parent → children) responses

    Used for endpoints that return related entities (e.g. work -> authors)
    Encodes parent context, child type, and pagination information

    :param parent_type: str, type of the parent entity (e.g. "work")
    :param parent_key: str, unique identifier of the parent entity
    :param child_type: str, type of related child entity (e.g. "author")
    :param total_children: int, total number of related child records available
    :param limit: int, maximum number of records returned in this response
    :param offset: int, pagination offset for the current response

    :return: dict, dictionary containing relationship metadata
    """
    return {
        'parent_type': parent_type,
        'parent_key': parent_key,
        'child_type': child_type,
        'total_children': total_children,
        'limit': limit,
        'offset': offset
    }

def build_batch_meta(
        entity_type: str,
        keys: list[str],
        total: int,
        limit: int,
        offset: int
) -> dict:
    """
    Build metadata for batch entity responses

    Used when multiple entities are fetched by a list of keys
    or search-like operations

    :param entity_type: str, type of entity being returned (e.g. "work", "author")
    :param keys: list[str], list of normalized entity keys used in the request
    :param total: int, total number of entities returned or matched
    :param limit: int, maximum number of records returned in this response
    :param offset: int, pagination offset for the current response

    :return: dict, dictionary containing batch metadata
    """
    return {
        'type': entity_type,
        'keys': keys,
        'total': total,
        'limit': limit,
        'offset': offset
    }