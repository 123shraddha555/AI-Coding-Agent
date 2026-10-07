from services import UserService


def test_create_user():
    service = UserService()

    user = service.create_user(
        "Shraddha",
        "shraddha@gmail.com"
    )

    assert user.name == "Shraddha"
    assert user.email == "shraddha@gmail.com"


def test_create_user_with_invalid_email():
    service = UserService()

    try:
        service.create_user(
            "Shraddha",
            "shraddha@example.com"
        )
        assert False
    except ValueError:
        assert True