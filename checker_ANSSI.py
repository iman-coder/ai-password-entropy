# checker.py
# ANSSI-aligned password checker (educational version)

import re
from collections import Counter

# --- Configuration (policy layer) ---
MIN_LENGTH = 12

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty",
    "azerty", "letmein", "admin", "welcome",
    "password123", "iloveyou"
}

# --- Helper functions ---

def is_long_enough(password: str) -> bool:
    return len(password) >= MIN_LENGTH


def is_common_password(password: str) -> bool:
    return password.lower() in COMMON_PASSWORDS


def has_low_entropy_pattern(password: str) -> bool:
    """
    Detects very weak patterns:
    - same character repeated
    - sequential numbers or letters
    """
    # Same character repeated
    if len(set(password)) == 1:
        return True

    # Numeric sequence
    if password.isdigit():
        return password in "0123456789" * 2

    # Alphabetical sequence
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    pwd = password.lower()
    return pwd in alphabet or pwd in alphabet[::-1]


def validate_password(password: str) -> list:
    """
    Returns a list of violations.
    Empty list = password is acceptable.
    """
    violations = []

    if not is_long_enough(password):
        violations.append("Password too short (minimum 12 characters)")

    if is_common_password(password):
        violations.append("Password is too common")

    if has_low_entropy_pattern(password):
        violations.append("Password has a very weak pattern")

    return violations


def check_password_group(passwords: list[str]) -> dict:
    """
    Validates a group of passwords and checks reuse.
    """
    results = {}
    counts = Counter(passwords)

    for pwd in passwords:
        violations = validate_password(pwd)

        if counts[pwd] > 1:
            violations.append("Password reused in the group")

        results[pwd] = {
            "valid": len(violations) == 0,
            "issues": violations
        }

    return results


# --- Example usage ---
if __name__ == "__main__":
    passwords = [
        "password123",
        "123456789012",
        "correct horse battery staple",
        "ordinateur-lampe-cafe-lion",
        "aaaaaaaaaaaa",
        "ordinateur-lampe-cafe-lion"
    ]

    report = check_password_group(passwords)

    for pwd, result in report.items():
        print(f"\nPassword: {pwd}")
        print("Valid:", result["valid"])
        if result["issues"]:
            for issue in result["issues"]:
                print(" -", issue)
