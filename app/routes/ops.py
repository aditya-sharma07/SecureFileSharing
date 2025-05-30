from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from app.models import FileUpload
from app import db
from app.utils.file_utils import allowed_file

ops_bp = Blueprint("ops", __name__)

@ops_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    user = get_jwt_identity()
    if user["role"] != "ops":
        return jsonify({"message": "Unauthorized"}), 403

    if 'file' not in request.files:
        return jsonify({"message": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    upload = FileUpload(filename=filename, uploaded_by=user["id"])
    db.session.add(upload)
    db.session.commit()

    return jsonify({"message": "File uploaded"}), 201
