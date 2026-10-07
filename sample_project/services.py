from models import User
from validators import validate_email, validate_name

class UserService:
    def __init__(self):
        self.users = []

    def create_user(self, name, email):
        if not validate_name(name):
            raise ValueError("Name cannot be empty.")

        if not validate_email(email):
            raise ValueError("Invalid or unsupported email address.")

        user = User(name, email)
        self.users.append(user)

        return user

    def get_all_users(self):
        return [user.to_dict() for user in self.users]