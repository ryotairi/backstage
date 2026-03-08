import secrets


def generate_user_id() -> int:
    """Generate a random 18-digit user ID."""
    digits = "".join(str(secrets.randbelow(10)) for _ in range(18))
    return int(digits)
