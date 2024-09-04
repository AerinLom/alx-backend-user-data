#!/usr/bin/env python3
"""
Auth module for managing API authentication.
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    Template class for all authentication systems
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path[-1] != '/':
                excluded_path += '/'
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from the request object.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user based on the request object.
        """
        return None

    def session_cookie(self, request=None):
        """
        """
        if request is None:
            return None
        cookie = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(cookie)
