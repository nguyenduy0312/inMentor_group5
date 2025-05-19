from flask import jsonify
from model.user import User
from database.connection import db # type: ignore
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

# Hàm đăng ký user mới
def register_user(data):
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not username or not email or not password:
        return jsonify({'message': 'Vui lòng cung cấp username, email và password'}), 400

    # Kiểm tra user đã tồn tại
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'message': 'Username hoặc email đã tồn tại'}), 409

    hashed_password = generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Đăng ký thành công'}), 201


# Hàm đăng nhập và trả về access + refresh token
def login_user(data):
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'message': 'Vui lòng cung cấp username và password'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Tên đăng nhập hoặc mật khẩu không đúng'}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'username': user.username
    }), 200


# Hàm refresh token lấy access token mới
@jwt_required(refresh=True)
def refresh_access_token():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': new_access_token}), 200


# Hàm logout (nếu có blacklist token, ở đây bạn có thể thêm logic xóa token)
def logout_user():
    # Cần hệ thống blacklist token để lưu token bị thu hồi (nếu muốn)
    # Nếu không dùng blacklist thì client chỉ việc xóa token
    return jsonify({'message': 'Đăng xuất thành công'}), 200
