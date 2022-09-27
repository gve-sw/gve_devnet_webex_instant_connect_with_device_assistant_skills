from flask import jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import admin_db
import uuid

class Admin:
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200
    
    def login(self):
        data = request.get_json()
        user = admin_db.users.find_one({"email": data['email']})

        if user and pbkdf2_sha256.verify(data['password'], user['password']):
            return self.start_session(user)
        
        return jsonify({"error": "Invalid login credentials"}), 401
    
    def logout(self):
        session.clear()
        print("clearing seesion")
        print(session)
        return redirect('/login')
