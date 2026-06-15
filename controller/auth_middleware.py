from functools import wraps
from flask import request, jsonify, g
from service import auth_service
from exception.app_exception import AppException


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token mancante!", "status": 401}), 401

        token = auth_header.split(" ", 1)[1]

        try:
            payload = auth_service.decode_token(token)
            g.current_user = payload
        except AppException as e:
            return jsonify(e.to_dict()), e.status_code

        return f(*args, **kwargs)

    return decorated


def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(g, "current_user") or g.current_user.get("role") != "admin":
            return jsonify({"error": "Accesso riservato agli amministratori!", "status": 403}), 403
        return f(*args, **kwargs)

    return decorated
