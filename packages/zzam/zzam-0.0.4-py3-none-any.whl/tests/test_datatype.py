from zzam.datatype import has_alphabetic_characters, has_numeric_characters


def test_has_alphabetic_characters():
    assert has_alphabetic_characters('1234F') == True


def test_not_has_alphabetic_characters():
    assert has_alphabetic_characters('12345') == False


def test_has_numeric_characters():
    assert has_numeric_characters('Hell0') == True


def test_not_has_numeric_characters():
    assert has_numeric_characters('Hello') == False
