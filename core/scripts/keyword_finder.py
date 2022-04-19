import re
import io


def find_keywords_in_text_file(keyword: str, output_format: str, text_file):
    """
    @param output_format:
    @param keyword: str
    @param text_file:
    @return: data
    """
    # Initiate the search
    keywords_found = re.findall(rf"\b{keyword}\w+", text_file)

    # Removing possible duplicates from array
    keys_without_duplicates = list(dict.fromkeys(keywords_found))

    # Getting the amount of keys occurrences
    keywords_amount_found = len(keys_without_duplicates)

    # Checking if keys are found
    result = {'keys_found': 0, 'data': []}
    if keywords_amount_found > 0:
        # Return desired output
        if output_format == 'outputinbrowser' or output_format == 'json':
            result['keys_found'] = keywords_amount_found
            result['data'] = keys_without_duplicates
            return result
        else:
            string_for_generation = ''
            for keyword in keys_without_duplicates:
                string_for_generation = string_for_generation + keyword + '\n'
            text_file_stream = io.StringIO(string_for_generation)
            return text_file_stream
    return result
