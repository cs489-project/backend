from flask import Blueprint, request, jsonify
from secrets import token_bytes
from argon2 import PasswordHasher
from db.models import User, Role
from db.client import db_client

users_bp = Blueprint('users', __name__)
ph = PasswordHasher()

def hash_password(password: str, salt: str) -> str:
    return ph.hash(password + salt)

def verify_password(hashed_password: str, password: str, salt: str) -> bool:
    try:
        ph.verify(hashed_password, password + salt)
        return True
    except:
        return False

def generate_salt() -> str:
    return token_bytes(32).hex()

@users_bp.route('/login-password', methods=['POST'])
def login_password():
    print('login-password')
    data = request.json
    email: str = data.get('email')
    password: str = data.get('password')

    user = db_client.session.query(User).filter_by(email=email).first()
    print('user', user)
    if not user:
        return jsonify({"error": "Error logging in"}), 401
    
    if not verify_password(user.password, password, user.salt):
        return jsonify({"error": "Error logging in"}), 401
    return jsonify({"message": "Logged in"}), 200


@users_bp.route('/login-mfa', methods=['POST'])
def login_mfa():
    data = request.json
    ...

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name: str = data.get('name')
    email: str = data.get('email')
    password: str = data.get('password')

    salt = generate_salt()
    print('generated', password, salt)
    hashed_password = hash_password(password, salt)
    user = User(name=name, email=email, password=hashed_password, salt=salt, role=Role.RESEARCHER)

    try:
        db_client.session.add(user)
        db_client.session.commit()
    except:
        return jsonify({"error": "Error registering"}), 400
    return jsonify({"message": "User created"}), 200
