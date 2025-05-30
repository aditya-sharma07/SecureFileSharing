from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, FileUpload
from app.utils.security import verify_token, generate_download_link
import os

client_bp = Blueprint("client", __name__)

@client_bp.route("/verify-email/<token>")
def verify_email(token):
    user_id = verify_token(token, type="verify")
    if not user_id:
        return jsonify({"message": "Invalid or expired token"}), 400

    user = User.query.get(user_id)
    if user:
        user.is_verified = True
        db.session.commit()
        return jsonify({"message": "Email verified!"})
    return jsonify({"message": "User not found"}), 404

@client_bp.route("/files", methods=["GET"])
@jwt_required()
def list_files():
    user = get_jwt_identity()
    if user["role"] != "client":
        return jsonify({"message": "Unauthorized"}), 403

    files = FileUpload.query.all()
    file_list = [{"id": f.id, "filename": f.filename, "uploaded_at": f.uploaded_at.isoformat()} for f in files]
    return jsonify(file_list)

@client_bp.route("/download/<int:file_id>", methods=["GET"])
@jwt_required()
def get_download_link(file_id):
    user = get_jwt_identity()
    if user["role"] != "client":
        return jsonify({"message": "Unauthorized"}), 403

    link = generate_download_link(file_id)
    return jsonify({"download_link": link})

@client_bp.route("/download-file/<token>", methods=["GET"])
@jwt_required()
def download_file(token):
    user = get_jwt_identity()
    if user["role"] != "client":
        return jsonify({"message": "Access denied"}), 403

    file_id = verify_token(token, type="download")
    file = FileUpload.query.get(file_id)
    if not file:
        return jsonify({"message": "File not found"}), 404

    return send_from_directory(current_app.config["UPLOAD_FOLDER"], file.filename, as_attachment=True)
