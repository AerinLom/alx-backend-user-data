#!/usr/bin/env python3
"""
Module for handling session authentication views.
"""
import os
from typing import Tuple
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user() -> Tuple[str, int]:
    """
    Handle user login and create a session.
    """
    email_not_found_response = {"error": "no user found for this email"}
    user_email = request.form.get('email')
    if not user_email or len(user_email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    
    user_password = request.form.get('password')
    if not user_password or len(user_password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        matched_users = User.search({'email': user_email})
    except Exception:
        return jsonify(email_not_found_response), 404

    if not matched_users:
        return jsonify(email_not_found_response), 404

    user = matched_users[0]

    if user.is_valid_password(user_password):
        from api.v1.app import auth
        
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        response.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return response
    
    return jsonify({"error": "wrong password"}), 401
