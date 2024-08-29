#!/usr/bin/env python3
"""
Module to handle password encryption.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with a salt using bcrypt.
    """
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a provided password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
