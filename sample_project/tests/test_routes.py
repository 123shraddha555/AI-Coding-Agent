from routers import UserRoutes


def test_register_user_successfully():
    routes = UserRoutes()

    result = routes.register_user(
        "Shraddha",
        "shraddha@gmail.com"
    )

    assert result["success"] is True
    assert result["user"]["name"] == "Shraddha"
    assert result["user"]["email"] == "shraddha@gmail.com"


def test_register_user_with_invalid_email():
    routes = UserRoutes()

    result = routes.register_user(
        "Shraddha",
        "shraddha@example.com"
    )

    assert result["success"] is False
    assert "Invalid" in result["message"]