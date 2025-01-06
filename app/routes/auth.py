from flask import Blueprint, request, jsonify
from app.models import User, UserBackground
from app.extensions import db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register a new user
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'email', 'password', 'background']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Validate background field
    allowed_backgrounds = [background.name.lower() for background in UserBackground]
    background = data.get('background', '').lower()
    if background not in allowed_backgrounds:
        return jsonify({"error": "Invalid background."}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Create a new user with the correct Enum value for background
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        background=UserBackground[background.upper()]  # Convert background to Enum
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# Login user
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({"message": "Logged in successfully!"}), 200

    return jsonify({"error": "Invalid credentials"}), 401

# Logout user
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"}), 200

# Get current user info
@auth_bp.route('/current_user', methods=['GET'])
@login_required
def current_user_info():
    return jsonify({
        "username": current_user.username,
        "email": current_user.email,
        "background": current_user.background.name  # Use .name to return the Enum's name
    }), 200

# Example of restricting access based on background
@auth_bp.route('/restricted', methods=['GET'])
@login_required
def restricted_access():
    allowed_backgrounds = ['researcher', 'activist']
    if current_user.background.name.lower() not in allowed_backgrounds:  # Access control with Enum names
        return jsonify({"error": "Access denied"}), 403

    return jsonify({"message": "Welcome to the restricted area!"}), 200
