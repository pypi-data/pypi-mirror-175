import re


def has_alphabetic_characters(value: str) -> bool:
    return bool(re.search(r'\D', value))


def has_numeric_characters(value: str) -> bool:
    return bool(re.search(r'[0-9]', value))
