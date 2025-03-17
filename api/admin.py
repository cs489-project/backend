from flask import Blueprint, request, jsonify
from db.models import AuthStage, User, Role
from db.client import db_client
from middleware.auth import SessionAuthStage, check_auth_stage, authenticate, check_roles

admin_bp = Blueprint('admin', __name__)

# TODO: test these endpoints

@admin_bp.route('/delete-user', methods=['POST'])
@authenticate()
@check_auth_stage()
@check_roles([Role.ADMIN])
def delete_user():
    data = request.json
    user_id: str = data.get('user_id')
    if not user_id:
        return jsonify({"error": "No ID provided"}), 400
    user = db_client.session.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    db_client.session.delete(user)
    db_client.session.commit()
    return jsonify({"message": "User deleted"}), 200


@admin_bp.route('/researchers', methods=['GET'])
@authenticate()
@check_roles([Role.ADMIN])
@check_auth_stage()
def researchers():
    users = db_client.session.query(User).filter_by(role=Role.RESEARCHER).all()
    return jsonify([{"name": user.name, "email": user.email, "id": user.id} for user in users]), 200

@admin_bp.route('/organizations', methods=['GET'])
@authenticate()
@check_auth_stage()
@check_roles([Role.ADMIN])
def organizations():
    users = db_client.session.query(User).filter_by(role=Role.ORGANIZATION).all()
    return jsonify([{"name": user.name, "email": user.email, "id": user.id} for user in users]), 200

@admin_bp.route('/user', methods=['GET'])
@authenticate()
@check_auth_stage()
@check_roles([Role.ADMIN])
def user():
    user_id: str = request.json.get('user_id')
    user = db_client.session.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "name": user.name, 
        "email": user.email, 
        "id": user.id,
        "auth_stage": user.auth_stage.value
    }), 200
