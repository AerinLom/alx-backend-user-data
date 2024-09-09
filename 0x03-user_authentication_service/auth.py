#!/usr/bin/env python3
"""
This module deals with Auth models
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of input password
    """
    hashed_bytes = password.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(hashed_bytes, bcrypt.gensalt())
    return hashed_pwd

class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user to the database
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")
