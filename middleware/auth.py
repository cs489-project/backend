from enum import Enum
from functools import wraps
from flask import request, jsonify
from db.models import AuthStage, User
from db.client import db_client
from redis_lib.session import SessionAuthStage, fetch_session

invalid_session = {"error": "Invalid session"}
invalid_permission = {"error": "Invalid permission"}


def min_auth_stage(auth_stage: AuthStage, minimum_auth_stage: AuthStage):
    stages = [AuthStage.PASSWORD, AuthStage.PENDING_MFA, AuthStage.MFA_VERIFIED, AuthStage.EMAIL_VERIFIED]
    return stages.index(auth_stage) >= stages.index(minimum_auth_stage)

def min_session_auth_stage(session_auth_stage: SessionAuthStage, minimum_session_auth_stage: SessionAuthStage):
    stages = [SessionAuthStage.PASSWORD, SessionAuthStage.MFA]
    return stages.index(session_auth_stage) >= stages.index(minimum_session_auth_stage)

def authenticate():
   def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_id = request.cookies.get("session_id")
        if not session_id:
            return jsonify(invalid_session), 400
        
        # Check if session ID exists in Redis
        session = fetch_session(session_id)
        if session is None:
            return jsonify(invalid_session), 400
        

        user = db_client.session.query(User).filter_by(id=session["user_id"]).first()
        if user is None:
            print("No user found for session", session)
            return jsonify(invalid_session), 400
        
        request.user = user
        request.session = session
        request.session_id = session_id
        return func(*args, **kwargs)
    return wrapper
   return decorator

def check_auth_stage(
        auth_stage: AuthStage = AuthStage.MFA_VERIFIED,  # minimum auth stage required
        session_auth_stage: SessionAuthStage = SessionAuthStage.MFA # minimum session auth stage required
    ):
   def decorator(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
            user = request.user
            session = request.session

            # Check for minimum session auth stage
            if not min_session_auth_stage(SessionAuthStage[session["auth_stage"]], session_auth_stage):
                return jsonify(invalid_permission), 403
            # Check for minimum auth stage
            if not min_auth_stage(user.auth_stage, auth_stage):
                return jsonify(invalid_permission), 401
            return func(*args, **kwargs)
      
       return wrapper
  
   return decorator


def check_roles(roles):
   def decorator(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
           user = request.user
           if not user:
                print("No user when checking roles for request", request)
                # internal server error
                return jsonify({"message": "Unauthorized"}), 500
           if user.role not in roles:
                return jsonify({"message": "Unauthorized"}), 403
          
           return func(*args, **kwargs)
      
       return wrapper
  
   return decorator
