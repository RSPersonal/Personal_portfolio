import random


def generate_random_number(range_start_for_numbers: int, range_end_for_numbers: int):
    """
    @param range_start_for_numbers:
    @param range_end_for_numbers:
    @return: random number between range
    """
    return random.randrange(range_start_for_numbers, range_end_for_numbers)

