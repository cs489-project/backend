from flask import Blueprint, request, jsonify
from db.models import AuthStage, User, Role
from db.client import db_client
from middleware.auth import SessionAuthStage, check_auth_stage, authenticate, check_roles
from util.auth import generate_salt, generate_totp_secret, get_totp_auth_uri, hash_password, verify_password, verify_totp

import redis_lib.session as session

users_bp = Blueprint('users', __name__)

login_error = {"error": "Error logging in"}
login_error_code = 401

@users_bp.route('/login-password', methods=['POST'])
def login_password():
    data = request.json
    email: str = data.get('email')
    password: str = data.get('password')

    if not email or not password:
        return jsonify(login_error), login_error_code

    user = db_client.session.query(User).filter_by(email=email).first()
    print('user', user)
    if not user:
        return jsonify(login_error), login_error_code
    
    if not verify_password(user.password, password, user.salt):
        return jsonify(login_error), login_error_code
    
    session_id = session.set_session_pending_mfa(user.id)
    response = jsonify({"message": "Logged in"})
    response.set_cookie('session_id', session_id, httponly=True, secure=True)
    return response, 200


@users_bp.route('/login-mfa', methods=['POST'])
@authenticate()
@check_auth_stage(auth_stage=AuthStage.PENDING_MFA, session_auth_stage=SessionAuthStage.PASSWORD)
def login_mfa():
    data = request.json
    code: str = data.get('code')
    if not code:
        return jsonify(login_error), login_error_code

    user: User = request.user
    session_id = request.session_id
    if not user.totp_secret:
        return jsonify(login_error), login_error_code
    if not verify_totp(user.totp_secret, code):
        return jsonify(login_error), login_error_code
    
    if user.auth_stage == AuthStage.PENDING_MFA:
        user.auth_stage = AuthStage.MFA_VERIFIED
        db_client.session.commit()
    session.set_session_mfa_verified(session_id)
    return jsonify({"message": "Logged in"}), 200

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name: str = data.get('name')
    email: str = data.get('email')
    password: str = data.get('password')
    # TODO: add password length check

    salt = generate_salt()
    print('generated', password, salt)
    hashed_password = hash_password(password, salt)
    user = User(name=name, email=email, password=hashed_password, salt=salt, role=Role.RESEARCHER)

    try:
        db_client.session.add(user)
        db_client.session.commit()
    except:
        return jsonify({"error": "Error registering"}), 400
    
    session_id = session.set_session_pending_mfa(user.id)
    response = jsonify({"message": "Registered"})
    response.set_cookie('session_id', session_id, httponly=True, secure=True)
    return response, 200


@users_bp.route('/register-mfa', methods=['POST'])
@authenticate()
def register_mfa():
    user: User = request.user
    secret = generate_totp_secret()
    uri = get_totp_auth_uri(user.email, secret)

    user.totp_secret = secret
    user.auth_stage = AuthStage.PENDING_MFA
    db_client.session.commit()
    return jsonify({"uri": uri}), 200


@users_bp.route('/logout', methods=['POST'])
@authenticate()
def logout():
    session.delete_session(request.session_id)
    return jsonify({"message": "Logged out"}), 200


@users_bp.route('/me', methods=['GET'])
@authenticate()
def me():
    user: User = request.user
    return jsonify({
        "name": user.name, 
        "email": user.email, 
        "role": user.role.value,
        "auth_stage": user.auth_stage.value
    }), 200

# sanity check routes
@users_bp.route('/check-admin-researcher', methods=['GET'])
@authenticate()
@check_roles([Role.ADMIN, Role.RESEARCHER])
def researcher_and_admin():
    return jsonify({"message": "Researcher and Admin"}), 200

@users_bp.route('/check-admin', methods=['GET'])
@authenticate()
@check_roles([Role.ADMIN])
def admin_only():
    return jsonify({"message": "Admin only"}), 200

@users_bp.route('/auth-stage', methods=['GET'])
@authenticate()
def auth_stage():
    user: User = request.user
    session: dict = request.session
    return jsonify({"auth_stage": user.auth_stage.value, "session_auth_stage": session["auth_stage"]}), 200
