# Helper class to check on standard input operation

def value(input_value):
    """
    Function to check if there is a value
    """
    if not no_value(input_value):
        return True
    else:
        return False


def no_value(input_value):
    """
    Function to check if there is no value
    """
    if input_value == '' or input_value == [] or input_value is None:
        return True
