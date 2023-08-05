def celsius2fahrenheit(celcius) -> float:
    """
    Handles the conversion from celcius to fahrenheint
    """
    return (float(celcius) * 9/5) + 32


def fahrenheit2celsius(fahrenheit) -> float:
    """
    Handles the conversion from fahrenheint to celcius
    """
    return (float(fahrenheit) - 32) * 5/9
