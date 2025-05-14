from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    identity = get_jwt_identity()
    user_id = identity['id']

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Kullanıcı bulunamadı."}), 404

    data = request.get_json()
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)

    if data.get('password'):
        user.set_password(data['password'])

    db.session.commit()

    return jsonify({"msg": "Profil güncellendi!"}), 200