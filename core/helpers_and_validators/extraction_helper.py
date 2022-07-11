import re


def extract_postal_code(dirty_postal_input: str):
    return re.search(r'\d{4}', dirty_postal_input).group(0)


if __name__ == '__main__':
    print(extract_postal_code("7951 BS"))
