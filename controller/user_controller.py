from flask import jsonify, request, Blueprint, g
from service import user_service
from exception.app_exception import AppException
from controller.auth_middleware import require_auth, require_admin

user_bp = Blueprint("user", __name__, url_prefix="/api")


# GET /api/users  — Solo admin
@user_bp.route("/users")
@require_auth
@require_admin
def get_users():
    users = user_service.get_all()
    return jsonify([u.to_dict() for u in users])


# GET /api/users/me  — Profilo utente loggato
@user_bp.route("/users/me")
@require_auth
def get_me():
    try:
        user = user_service.get_by_id(g.current_user["user_id"])
        return jsonify(user.to_dict())

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# GET /api/users/<id>
@user_bp.route("/users/<int:user_id>")
@require_auth
def get_user_by_id(user_id):
    try:
        if g.current_user["role"] != "admin" and g.current_user["user_id"] != user_id:
            raise AppException("Non sei autorizzato!", 403)

        user = user_service.get_by_id(user_id)
        return jsonify(user.to_dict())

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# PATCH /api/users/<id>
@user_bp.route("/users/<int:user_id>", methods=["PATCH"])
@require_auth
def update(user_id):
    data = request.get_json()

    try:
        updated = user_service.update(
            user_id,
            data,
            requesting_user_id=g.current_user["user_id"],
            is_admin=(g.current_user["role"] == "admin")
        )
        return jsonify(updated.to_dict())

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# DELETE /api/users/<id>  — Solo admin
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@require_auth
@require_admin
def delete_user_by_id(user_id):
    try:
        user_service.delete_by_id(user_id)
        return jsonify({"message": "Utente eliminato con successo"})

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code
