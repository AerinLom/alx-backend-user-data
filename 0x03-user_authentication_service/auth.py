#!/usr/bin/env python3
"""
This module deals with Auth models
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of input password
    """
    hashed_bytes = password.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(hashed_bytes, bcrypt.gensalt())
    return hashed_pwd

def _generate_uuid() -> str:
    """
    Generates a uuid and returns it as a string
    """
    uuid_string = str(uuid.uuid4())
    return uuid_string


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates input user credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password
            )
        except NoResultFound:
            return False
