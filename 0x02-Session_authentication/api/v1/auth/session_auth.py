#!/usr/bin/env python3
"""
SessionAuth module for managing session authentication.
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    Template class for session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new session ID for a given user ID
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with session ID.
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the current user based on the session ID
        """
        if request is None:
            return None
        sess_id = self.session_cookie(request)
        if sess_id is None:
            return None

        user_id = self.user_id_for_session_id(sess_id)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroy the user session / logout."""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
