#!/usr/bin/env python3
"""
This module sets up a basic Flask app.
"""
from flask import Flask, jsonify, request, abort
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    Logs in a user and creates a session.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    Logs user out of session
    """
    session_id = request.cookies.get("session_id")
    logged_out_user = AUTH.get_user_from_session_id(session_id)
    if logged_out_user is None:
        abort(403)
    AUTH.destroy_session(logged_out_user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
