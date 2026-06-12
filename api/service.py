"""
Transformation utilities for formatting database query results
"""

def format_records(
        records: list | None,
        fields: list[str] | None
) -> list:
    """
    Formats list of records into a list of dictionaries

    :param records: list, list of records containing values
    :param fields: list[str], list of field names corresponding to each value in a record
    :return: list, list of dictionaries mapping field names to record values
                   Returns an empty list if the input is invalid
    """
    # In case no records or fields were passed then return empty list
    if not records or not fields:
        return []

    # Set up results list
    results = []

    # For each record make a zip object of each field and value
    for record in records:

        # In case no the same amount of record values and fields are
        # given then return empty list
        if len(record) != len(fields):
            return []

        # Add to the results list the zip
        results.append(dict(zip(fields, record)))

    # return results
    return results

def format_response(
        query: str,
        endpoint: str,
        method: str,
        records: list | None = None,
        column_names: list[str] | None = None
) -> dict:
    """
    Formats the API's final response

    :param query: str, the query used for the API
    :param endpoint: str, the endpoing used for quering the API
    :param method: str, HTTP method used (GET, POST, PUT, DELETE, PATCH, OPTIONS, and HEAD)
    :param records: list, list of records containing values
    :param column_names: list[str], list of column names corresponding to each value in a record

    :return: dict, dictionary mapping the API's responce
    """
    if records is None:
        records = []

    formatted_records = format_records(records, column_names)

    return {
        'query': query,
        'endpoint': endpoint,
        'method': method,
        'count': len(formatted_records),
        'results': formatted_records
    }
