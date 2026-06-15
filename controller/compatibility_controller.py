from flask import jsonify, request, Blueprint
from service import compatibility_service
from exception.app_exception import AppException
from controller.auth_middleware import require_auth, require_admin

compatibility_bp = Blueprint("compatibility", __name__, url_prefix="/api")


# GET /api/compatibility-rules
@compatibility_bp.route("/compatibility-rules")
def get_rules():
    rules = compatibility_service.get_all()
    return jsonify([r.to_dict() for r in rules])


# POST /api/compatibility-rules  — Solo admin
@compatibility_bp.route("/compatibility-rules", methods=["POST"])
@require_auth
@require_admin
def create():
    data = request.get_json()

    try:
        rule = compatibility_service.create(data)
        return jsonify(rule.to_dict()), 201

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# PATCH /api/compatibility-rules/<id>  — Solo admin
@compatibility_bp.route("/compatibility-rules/<int:rule_id>", methods=["PATCH"])
@require_auth
@require_admin
def update(rule_id):
    data = request.get_json()

    try:
        updated = compatibility_service.update(rule_id, data)
        return jsonify(updated.to_dict())

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# DELETE /api/compatibility-rules/<id>  — Solo admin
@compatibility_bp.route("/compatibility-rules/<int:rule_id>", methods=["DELETE"])
@require_auth
@require_admin
def delete_rule_by_id(rule_id):
    try:
        compatibility_service.delete_by_id(rule_id)
        return jsonify({"message": "Regola eliminata con successo"})

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# POST /api/compatibility-check
# Body: { "component_ids": [1, 2, 3] }
@compatibility_bp.route("/compatibility-check", methods=["POST"])
def check_compatibility():
    data = request.get_json()

    try:
        component_ids = data.get("component_ids", [])
        if not isinstance(component_ids, list):
            raise AppException("'component_ids' deve essere una lista!", 400)

        result = compatibility_service.check_compatibility(component_ids)
        return jsonify(result)

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code


# GET /api/compatible-components?component_id=1&category=Motherboard
@compatibility_bp.route("/compatible-components")
def get_compatible_components():
    try:
        component_id = request.args.get("component_id", type=int)
        category = request.args.get("category")

        if not component_id:
            raise AppException("Parametro 'component_id' obbligatorio!", 400)
        if not category:
            raise AppException("Parametro 'category' obbligatorio!", 400)

        components = compatibility_service.get_compatible_components(component_id, category)
        return jsonify([c.to_dict() for c in components])

    except AppException as e:
        return jsonify(e.to_dict()), e.status_code
