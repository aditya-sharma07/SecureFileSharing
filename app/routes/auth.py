from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from flask_jwt_extended import create_access_token
from app.utils.security import generate_verification_link
from app.utils.email_utils import send_verification_email

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered"}), 400

    hashed = generate_password_hash(data["password"])
    user = User(email=data["email"], password=hashed, role="client")
    db.session.add(user)
    db.session.commit()

    link = generate_verification_link(user.id)
    send_verification_email(user.email, link)

    return jsonify({"message": "Verification email sent"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity={"id": user.id, "role": user.role})
    return jsonify({"token": token, "role": user.role}), 200
