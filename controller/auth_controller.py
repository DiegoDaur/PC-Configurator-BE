from flask import jsonify, request, Blueprint
from service import auth_service
from exception.app_exception import AppException

auth_bp = Blueprint("auth", __name__, url_prefix="/api")


# POST /api/auth/register
@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    try:
        new_user = auth_service.register(data)
        return jsonify(new_user.to_dict()), 201

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# POST /api/auth/login
@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    try:
        result = auth_service.login(data)
        return jsonify({
            "user":  result["user"].to_dict(),
            "token": result["token"],
        })

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code
