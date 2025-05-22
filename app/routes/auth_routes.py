@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')  # Added username field
    role = data.get('role')  # "customer" veya "supplier"

    if not all([email, password, role]):
        return jsonify({"msg": "Eksik bilgi var."}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "Bu email zaten kullanılıyor."}), 409

    user = User(
        email=email,
        first_name=username,  # Using username as first_name
        role=role
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Kayıt başarılı!"}), 201 