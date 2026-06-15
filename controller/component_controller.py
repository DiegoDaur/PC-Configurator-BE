from flask import jsonify, request, Blueprint
from service import component_service
from exception.app_exception import AppException
from controller.auth_middleware import require_auth, require_admin

component_bp = Blueprint("component", __name__, url_prefix="/api")


# GET /api/components?category=CPU
@component_bp.route("/components")
def get_components():
    category = request.args.get("category")

    try:
        components = component_service.get_all(category)
        return jsonify([c.to_dict() for c in components])

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# GET /api/components/<id>
@component_bp.route("/components/<int:component_id>")
def get_component_by_id(component_id):
    try:
        component = component_service.get_by_id(component_id)
        return jsonify(component.to_dict())

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# POST /api/components  — Solo admin
@component_bp.route("/components", methods=["POST"])
@require_auth
@require_admin
def create():
    data = request.get_json()

    try:
        new_component = component_service.create(data)
        return jsonify(new_component.to_dict()), 201

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# PATCH /api/components/<id>  — Solo admin
@component_bp.route("/components/<int:component_id>", methods=["PATCH"])
@require_auth
@require_admin
def update(component_id):
    data = request.get_json()

    try:
        updated = component_service.update(component_id, data)
        return jsonify(updated.to_dict())

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# DELETE /api/components/<id>  — Solo admin
@component_bp.route("/components/<int:component_id>", methods=["DELETE"])
@require_auth
@require_admin
def delete_component_by_id(component_id):
    try:
        component_service.delete_by_id(component_id)
        return jsonify({"message": "Componente eliminato con successo"})

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code
