import json

def load_json(filename: str):
    """
    Helper function for loading JSON files
    :param filename:
    :return:
    """
    with open(filename, mode='r', encoding='utf-8') as j:
        data = json.load(j)

    return data

def save_json(
        data: dict | list[str] | None,
        filename: str
) -> None:
    """
    Helper function for saving response as JSON files
    :param data: dict | list[str] | None, containing the response from the API
    :param filename: str, the file name or path for saving the file
    :return: None
    """

    # In case no data was returned then a ValueError is raised
    if data is None:
        raise ValueError(f'No data was returned for query!')

    # Is case the another type is used for saving the data ValueError is raised
    if not filename.endswith('.json'):
        raise ValueError("File must be a JSON file")

    # Saving the data as a JSON file with pretty print (intent: 4 space)
    with open(filename, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
