from model.build import Build
from repository import build_repository, component_repository
from exception.app_exception import AppException


def get_all():
    return build_repository.get_all()


def get_by_id(build_id):
    build = build_repository.get_by_id(build_id)
    if build is None:
        raise AppException("Configurazione non trovata!", 404)
    return build


def get_by_user(user_id):
    return build_repository.get_by_user_id(user_id)


def create(data, user_id):
    _validate_build(data)

    components = _resolve_components(data.get("component_ids", []))

    new_build = Build(
        id=None,
        user_id=user_id,
        name=data["name"],
        notes=data.get("notes"),
        created_at=None,
        components=components,
    )

    return build_repository.create(new_build)


def update(build_id, data, user_id):
    build = build_repository.get_by_id(build_id)
    if build is None:
        raise AppException("Configurazione non trovata!", 404)

    if build.user_id != user_id:
        raise AppException("Non sei autorizzato a modificare questa configurazione!", 403)

    new_components = None
    if "component_ids" in data:
        new_components = _resolve_components(data["component_ids"])

    return build_repository.update(build_id, data, new_components)


def delete_by_id(build_id, user_id, is_admin=False):
    build = build_repository.get_by_id(build_id)
    if build is None:
        raise AppException("Configurazione non trovata!", 404)

    if build.user_id != user_id and not is_admin:
        raise AppException("Non sei autorizzato a eliminare questa configurazione!", 403)

    build_repository.delete_by_id(build_id)


def compare(build_id_1, build_id_2):
    build1 = get_by_id(build_id_1)
    build2 = get_by_id(build_id_2)

    return {
        "build1": build1.to_dict(),
        "build2": build2.to_dict(),
        "diff": {
            "price_diff":   round(build1.total_price() - build2.total_price(), 2),
            "wattage_diff": build1.total_wattage() - build2.total_wattage(),
        }
    }


def _resolve_components(component_ids):
    if not component_ids:
        return []
    components = component_repository.get_by_ids(component_ids)
    found_ids = {c.id for c in components}
    missing = set(component_ids) - found_ids
    if missing:
        raise AppException(f"Componenti non trovati: {sorted(missing)}", 404)
    return components


def _validate_build(data):
    if "name" not in data or not str(data["name"]).strip():
        raise AppException("Campo 'name' obbligatorio!", 400)
    if len(data["name"]) < 3:
        raise AppException("Il nome della configurazione deve avere almeno 3 caratteri!", 400)
