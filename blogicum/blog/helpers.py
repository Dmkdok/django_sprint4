from django.utils.text import Truncator


def truncate_string(input_string, max_length):
    """Обрезает строку до указанной длины."""
    return Truncator(input_string).chars(max_length)
