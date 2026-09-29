import secrets
import string

def generate_password(length=16):
    """
    Generate a cryptographically secure random password.
    """
    alphabet = (
        string.ascii_lowercase +
        string.ascii_uppercase +
        string.digits +
        string.punctuation
    )

    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_multiple_passwords(count=1000, length=16):
    """
    Generate multiple cryptographically secure passwords.
    """
    return [generate_password(length) for _ in range(count)]


if __name__ == "__main__":
    passwords = generate_multiple_passwords(count=1000, length=16)
    for p in passwords:
        print(p)
