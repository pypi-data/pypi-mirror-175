from zzam.temperature import fahrenheit2celsius, celsius2fahrenheit


def test_fahrenheit2celsius():
    assert fahrenheit2celsius(32) == 0.0


def test_celsius2fahrenheit():
    assert celsius2fahrenheit(0) == 32
