# Helper file to check on standard input operation

def value(input_value):
    """
    @param input_value:
    @return: bool
    """
    if not no_value(input_value):
        return True
    return False


def no_value(input_value):
    """
    @param input_value:
    @return: bool
    """
    if input_value == '' or input_value == [] or input_value is None:
        return True
