"""
Utility for splitting lists into fixed-size batches.
"""

def make_batches(lst: list[str], batch_size: int) -> list[list[str]]:
    """
    Make batches from list using a predetermined batch size
    :param lst: list, the list to make batches from
    :param batch_size: int, the batch size for the batches
    :return: list[list[str]], the list containing the batches as lists of strings
    """

    batches = [
        lst[i: i + batch_size]
        for i in range(0, len(lst), batch_size)
    ]

    return  batches