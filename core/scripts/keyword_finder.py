import re


def find_keywords_in_text_file(keyword: str, text_file):
    """
    @param keyword: str
    @param text_file:
    @return: data
    """
    # Initiate the search
    keywords_found = re.findall(rf"\b{keyword}\w+", text_file)

    # Removing possible duplicates from array
    keys_without_duplicates = list(dict.fromkeys(keywords_found))

    # Getting the amount of keys finds
    keywords_amount_found = len(keys_without_duplicates)

    # Checking if keys are found
    result = {'keys_found': 0, 'data': []}
    if keywords_amount_found > 0:
        result['keys_found'] = str(keywords_amount_found)
        result['data'] = keys_without_duplicates
    return result
