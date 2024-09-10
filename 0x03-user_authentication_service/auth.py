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

    def create_session(self, email: str) -> str:
        """
        Creates a session for a user and assigns a uuid
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Returns a user based off of the session id or none
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a users session
        """
        if user_id is None:
            return None
        clear_id = None
        self._db.update_user(user_id, session_id=clear_id)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            new_reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=new_reset_token)
            return new_reset_token
        except Exception:
            raise ValueError
