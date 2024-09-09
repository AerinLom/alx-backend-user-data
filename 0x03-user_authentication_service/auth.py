#!/usr/bin/env python3
"""
This module deals with Auth models
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of input password
    """
    hashed_bytes = password.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(hashed_bytes, bcrypt.gensalt())
    return hashed_pwd
