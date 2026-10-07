from validators import validate_email, validate_name


def test_valid_email():
    assert validate_email("user@gmail.com") is True


def test_invalid_email():
    assert validate_email("user@example.com") is False


def test_empty_name():
    assert validate_name("") is False


def test_valid_name():
    assert validate_name("Shraddha") is True