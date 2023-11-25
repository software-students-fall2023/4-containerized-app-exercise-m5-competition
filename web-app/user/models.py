"""import utilities and db"""
from flask import jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db

class User:
    """Utility functions for user"""

    def start_session(self, user):
        """Create session containing user info"""
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        """signing up"""
        print(request.form)

        # Create the user object
        user = {
          "username": request.form.get('username'),
          "password": request.form.get('password')
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing username address
        if db.users.find_one({ "usernmae": user['username'] }):
            return jsonify({ "error": "Username already in use" }), 400

        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({ "error": "Signup failed" }), 400

    def signout(self):
        """signing out"""
        session.clear()
        return redirect('/')

    def login(self):
        """logging in """
        user = db.users.find_one({
            "username": request.form.get('username')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({ "error": "Invalid login credentials" }), 401
