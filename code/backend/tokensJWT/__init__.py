from functools import wraps
from flask import jsonify, request
from routes import app
import jwt
import datetime

SECRET_KEY = app.config["SECRET_KEY"]

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.admin_name = payload["name"]
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
    
    return decorated

def admin_token(admin_name):
    token = jwt.encode(
        {
            "name": admin_name,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    
    return token

def user_token(user_name):
    token = jwt.encode(
        {
            "name": user_name,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return token