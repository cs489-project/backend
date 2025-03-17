from enum import Enum
from functools import wraps
from flask import request, jsonify
from db.models import AuthStage, User
from db.client import db_client
from redis_lib import redis_client

class SessionAuthStage(Enum):
   NONE = 0
   PASSWORD = 1
   MFA = 2

def authenticate(
      auth_stage: AuthStage = AuthStage.MFA_VERIFIED, 
      session_auth_stage: SessionAuthStage = SessionAuthStage.MFA
    ):
   def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("authenticating middleware for", auth_stage, args, kwargs)
        # TODO: remove this to check for session after session is implemented, let all requests pass for now
        data = request.json
        user = db_client.session.query(User).filter_by(email=data.get("email")).first()
        request.user = user

        return func(*args, **kwargs)
        session_id = request.cookies.get("session_id")
        if not session_id:
            return jsonify({"error": "Unauthorized: No session ID"}), 401
        

        # Check if session ID exists in Redis
        user_id = redis_client.get(f"session:{session_id}")

        # Check for auth stage
        


            # TODO: add another check for 2fa
        if not user_id:
            return jsonify({"error": "Unauthorized: Invalid session"}), 401
        
        request.user_id = user_id
        return func(*args, **kwargs)
    return wrapper
   return decorator


def check_role(roles):
   def decorator(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
           user = request.user
           if user.role not in roles:
               return jsonify({"message": "Unauthorized"}), 403
          
           return func(*args, **kwargs)
      
       return wrapper
  
   return decorator
