from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def get_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

def generate_verification_link(user_id):
    s = get_serializer()
    token = s.dumps(user_id, salt=current_app.config["VERIFICATION_URL_SALT"])
    return f"http://localhost:5000/client/verify-email/{token}"

def generate_download_link(file_id):
    s = get_serializer()
    token = s.dumps(file_id, salt=current_app.config["DOWNLOAD_URL_SALT"])
    return f"http://localhost:5000/client/download-file/{token}"

def verify_token(token, type="download"):
    s = get_serializer()
    try:
        salt = current_app.config["DOWNLOAD_URL_SALT"] if type == "download" else current_app.config["VERIFICATION_URL_SALT"]
        max_age = current_app.config["DOWNLOAD_URL_EXPIRATION"] if type == "download" else current_app.config["VERIFICATION_URL_EXPIRATION"]
        return s.loads(token, salt=salt, max_age=max_age)
    except Exception:
        return None
