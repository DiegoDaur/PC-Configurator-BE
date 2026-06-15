from sqlalchemy import text
from persistence.db_config import get_session
from model.component import Component


def _row_to_component(row):
    specs = {}
    if row.specs:
        for pair in row.specs.split("|"):
            if ":" in pair:
                k, v = pair.split(":", 1)
                specs[k.strip()] = v.strip()

    return Component(
        id=row.id,
        name=row.name,
        brand=row.brand,
        category=row.category,
        price=row.price,
        wattage=row.wattage,
        stock=row.stock,
        in_stock=row.in_stock,
        image_url=row.image_url,
        description=row.description,
        specs=specs,
    )


def _specs_to_str(specs_dict):
    if not specs_dict:
        return None
    return "|".join(f"{k}:{v}" for k, v in specs_dict.items())


def create(component):
    session = get_session()

    result = session.execute(
        text(
            "INSERT INTO component (name, brand, category, price, wattage, stock, in_stock, image_url, description, specs) "
            "VALUES (:name, :brand, :category, :price, :wattage, :stock, :in_stock, :image_url, :description, :specs) "
            "RETURNING id"
        ),
        {
            "name":        component.name,
            "brand":       component.brand,
            "category":    component.category,
            "price":       component.price,
            "wattage":     component.wattage,
            "stock":       component.stock,
            "in_stock":    component.in_stock,
            "image_url":   component.image_url,
            "description": component.description,
            "specs":       _specs_to_str(component.specs),
        }
    )
    session.commit()
    component.id = result.fetchone()[0]
    session.close()

    return component


def get_all():
    session = get_session()
    rows = session.execute(text("SELECT * FROM component")).fetchall()
    session.close()
    return [_row_to_component(r) for r in rows]


def get_by_id(component_id):
    session = get_session()
    row = session.execute(
        text("SELECT * FROM component WHERE id = :id"),
        {"id": component_id}
    ).fetchone()
    session.close()

    if row is None:
        return None
    return _row_to_component(row)


def get_by_category(category):
    session = get_session()
    rows = session.execute(
        text("SELECT * FROM component WHERE category = :category"),
        {"category": category}
    ).fetchall()
    session.close()
    return [_row_to_component(r) for r in rows]


def get_by_ids(ids):
    if not ids:
        return []
    session = get_session()
    rows = session.execute(
        text("SELECT * FROM component WHERE id = ANY(:ids)"),
        {"ids": list(ids)}
    ).fetchall()
    session.close()
    return [_row_to_component(r) for r in rows]


def update(component_id, data):
    session = get_session()

    fields = []
    params = {"id": component_id}

    for campo in ["name", "brand", "price", "wattage", "stock", "in_stock", "image_url", "description"]:
        if campo in data:
            fields.append(f"{campo} = :{campo}")
            params[campo] = data[campo]

    if "specs" in data:
        fields.append("specs = :specs")
        params["specs"] = _specs_to_str(data["specs"])

    if not fields:
        session.close()
        return get_by_id(component_id)

    session.execute(
        text(f"UPDATE component SET {', '.join(fields)} WHERE id = :id"),
        params
    )
    session.commit()
    session.close()

    return get_by_id(component_id)


def delete_by_id(component_id):
    session = get_session()
    session.execute(text("DELETE FROM component WHERE id = :id"), {"id": component_id})
    session.commit()
    session.close()
