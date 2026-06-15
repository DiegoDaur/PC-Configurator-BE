from flask import jsonify, request, Blueprint, g
from service import build_service
from exception.app_exception import AppException
from controller.auth_middleware import require_auth, require_admin

build_bp = Blueprint("build", __name__, url_prefix="/api")


# GET /api/builds  — Admin: tutte le build; Utente: solo le proprie
@build_bp.route("/builds")
@require_auth
def get_builds():
    if g.current_user["role"] == "admin":
        builds = build_service.get_all()
    else:
        builds = build_service.get_by_user(g.current_user["user_id"])

    return jsonify([b.to_dict() for b in builds])


# GET /api/builds/compare?build1=1&build2=2
@build_bp.route("/builds/compare")
@require_auth
def compare_builds():
    try:
        build_id_1 = request.args.get("build1", type=int)
        build_id_2 = request.args.get("build2", type=int)

        if not build_id_1 or not build_id_2:
            raise AppException("Parametri 'build1' e 'build2' obbligatori!", 400)

        result = build_service.compare(build_id_1, build_id_2)
        return jsonify(result)

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# GET /api/builds/<id>
@build_bp.route("/builds/<int:build_id>")
@require_auth
def get_build_by_id(build_id):
    try:
        build = build_service.get_by_id(build_id)

        if g.current_user["role"] != "admin" and build.user_id != g.current_user["user_id"]:
            raise AppException("Non sei autorizzato a visualizzare questa configurazione!", 403)

        return jsonify(build.to_dict())

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# POST /api/builds
@build_bp.route("/builds", methods=["POST"])
@require_auth
def create():
    data = request.get_json()

    try:
        new_build = build_service.create(data, g.current_user["user_id"])
        return jsonify(new_build.to_dict()), 201

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# PATCH /api/builds/<id>
@build_bp.route("/builds/<int:build_id>", methods=["PATCH"])
@require_auth
def update(build_id):
    data = request.get_json()

    try:
        updated = build_service.update(build_id, data, g.current_user["user_id"])
        return jsonify(updated.to_dict())

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# DELETE /api/builds/<id>
@build_bp.route("/builds/<int:build_id>", methods=["DELETE"])
@require_auth
def delete_build_by_id(build_id):
    try:
        build_service.delete_by_id(
            build_id,
            user_id=g.current_user["user_id"],
            is_admin=(g.current_user["role"] == "admin")
        )
        return jsonify({"message": "Configurazione eliminata con successo"})

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code
