#!/usr/bin/env python3
"""
bcrypt password hashing
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with salt.

    Returns:
        bytes: The salted, hashed password as a byte string.

    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates a password against a hashed password using bcrypt.

    Returns:
        bool: True if the password matches the hashed password,
        False otherwise.

    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
