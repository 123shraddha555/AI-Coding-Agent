from routers import UserRoutes


def main():
    user_routes = UserRoutes()

    result = user_routes.register_user(
        "Shraddha",
        "shraddha@gmail.com"
    )

    print(result)

    print("\nAll users:")
    print(user_routes.get_users())


if __name__ == "__main__":
    main()