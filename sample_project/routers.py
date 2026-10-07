from services import UserService


class UserRoutes:
    def __init__(self):
        self.user_service = UserService()

    def register_user(self, name, email):
        try:
            user = self.user_service.create_user(name, email)

            return {
                "success": True,
                "message": "User registered successfully.",
                "user": user.to_dict()
            }

        except ValueError as error:
            return {
                "success": False,
                "message": str(error)
            }

    def get_users(self):
        return {
            "success": True,
            "users": self.user_service.get_all_users()
        }