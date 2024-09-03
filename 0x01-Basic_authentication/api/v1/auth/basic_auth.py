#!/usr/bin/env python3
"""
BasicAuth module for managing basic authentication.
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Template class for basic authentication
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Returns Base64 auth header for basic authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]
