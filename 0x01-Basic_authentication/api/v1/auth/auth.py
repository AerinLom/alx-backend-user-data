#!/usr/bin/env python3
"""
Auth module for managing API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Template class for all authentication systems
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from the request object.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user based on the request object.
        """
        return None
