from model.component import Component, VALID_CATEGORIES
from repository import component_repository
from exception.app_exception import AppException


def get_all(category=None):
    if category:
        if category not in VALID_CATEGORIES:
            raise AppException(f"Categoria '{category}' non valida. Valide: {', '.join(VALID_CATEGORIES)}", 400)
        return component_repository.get_by_category(category)
    return component_repository.get_all()


def get_by_id(component_id):
    component = component_repository.get_by_id(component_id)
    if component is None:
        raise AppException("Componente non trovato!", 404)
    return component


def create(data):
    _validate_component(data)

    new_component = Component(
        id=None,
        name=data["name"],
        brand=data["brand"],
        category=data["category"],
        price=float(data["price"]),
        wattage=int(data.get("wattage", 0)),
        stock=int(data.get("stock", 0)),
        in_stock=bool(data.get("in_stock", True)),
        image_url=data.get("image_url"),
        description=data.get("description"),
        specs=data.get("specs", {}),
    )

    return component_repository.create(new_component)


def update(component_id, data):
    if component_repository.get_by_id(component_id) is None:
        raise AppException("Componente non trovato!", 404)

    if "category" in data:
        raise AppException("La categoria di un componente non può essere modificata!", 400)

    return component_repository.update(component_id, data)


def delete_by_id(component_id):
    if component_repository.get_by_id(component_id) is None:
        raise AppException("Componente non trovato!", 404)
    component_repository.delete_by_id(component_id)


def _validate_component(data):
    for campo in ["name", "brand", "category", "price"]:
        if campo not in data or not str(data[campo]).strip():
            raise AppException(f"Campo '{campo}' obbligatorio!", 400)

    if data["category"] not in VALID_CATEGORIES:
        raise AppException(
            f"Categoria '{data['category']}' non valida. Valide: {', '.join(VALID_CATEGORIES)}", 400
        )

    try:
        price = float(data["price"])
        if price < 0:
            raise ValueError
    except (ValueError, TypeError):
        raise AppException("Il prezzo deve essere un numero positivo!", 400)
