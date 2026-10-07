from config import ALLOWED_EMAIL_DOMAINS


def validate_email(email):
    """Validate email format and allowed domain."""
    if not email or "@" not in email:
        return False

    domain = email.split("@")[-1].lower()

    if domain not in ALLOWED_EMAIL_DOMAINS:
        return False

    return True


def validate_name(name):
    """Validate that the user's name is not empty."""
    return bool(name and name.strip())