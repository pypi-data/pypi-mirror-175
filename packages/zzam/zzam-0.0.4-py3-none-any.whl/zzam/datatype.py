import re


def has_alphabetic_characters(value: str) -> bool:
    """
    Handles checking if the requested string is only made by numbers or not
    """
    return bool(re.search(r'\D', value))


def has_numeric_characters(value: str) -> bool:
    """
    Handles checking if the requested string is only made by alphabetical
    characters (letters) or not
    """
    return bool(re.search(r'[0-9]', value))
