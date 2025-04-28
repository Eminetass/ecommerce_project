from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token
from app.utils.mailer import send_reset_email
import secrets



auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    role = data.get('role')  # "customer" veya "supplier"

    if not all([email, password, role]):
        return jsonify({"msg": "Eksik bilgi var."}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "Bu email zaten kullanılıyor."}), 409

    user = User(email=email, first_name=first_name, last_name=last_name, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Kayıt başarılı!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Hatalı giriş."}), 401

    access_token = create_access_token(identity={"id": user.id, "role": user.role})


    return jsonify(access_token=access_token), 200

reset_tokens = {}  # Basit token kaydı (ileride Redis gibi sistemler önerilir)

@auth_bp.route('/reset-password-request', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "Email bulunamadı."}), 404

    token = secrets.token_urlsafe(16)
    reset_tokens[token] = user.id

    send_reset_email(user.email, token)

    return jsonify({"msg": "Şifre sıfırlama bağlantısı gönderildi."}), 200


@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    if token not in reset_tokens:
        return jsonify({"msg": "Geçersiz veya süresi dolmuş token."}), 400

    user_id = reset_tokens[token]
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "Kullanıcı bulunamadı."}), 404

    data = request.get_json()
    new_password = data.get('password')

    if not new_password:
        return jsonify({"msg": "Yeni şifre gerekli."}), 400

    user.set_password(new_password)
    db.session.commit()

    reset_tokens.pop(token)  # Token bir kere kullanıldıktan sonra sil

    return jsonify({"msg": "Şifre başarıyla sıfırlandı!"}), 200