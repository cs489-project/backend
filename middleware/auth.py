from functools import wraps
from flask import request, jsonify
from redis_lib import redis_client

def authenticate(f):
   def wrapper(*args, **kwargs):
       session_id = request.cookies.get("session_id")
       if not session_id:
           return jsonify({"error": "Unauthorized: No session ID"}), 401
       

       # Check if session ID exists in Redis
       user_id = redis_client.get(f"session:{session_id}")


        # TODO: add another check for 2fa
       if not user_id:
           return jsonify({"error": "Unauthorized: Invalid session"}), 401
	
       request.user_id = user_id
       return f(*args, **kwargs)


   return wrapper


def check_role(roles):
   def decorator(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
           user = request.current_user
           if user.role not in roles:
               return jsonify({"message": "Unauthorized"}), 403
          
           return func(*args, **kwargs)
      
       return wrapper
  
   return decorator
