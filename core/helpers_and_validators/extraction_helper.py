import re


def extract_postal_code(dirty_postal_input: str):
    """
    @param dirty_postal_input:
    @return:
    """
    return re.search(r'\d{4}', dirty_postal_input).group(0)
