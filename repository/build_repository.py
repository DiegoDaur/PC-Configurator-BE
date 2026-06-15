from flask import session
from sqlalchemy import text
from persistence.db_config import get_session
from model.build import Build
from repository import component_repository


def _load_build(row):
    session = get_session()
    comp_rows = session.execute(
        text("SELECT component_id FROM build_component WHERE build_id = :id"),
        {"id": row.id}
    ).fetchall()
    session.close()

    component_ids = [r.component_id for r in comp_rows]
    components = component_repository.get_by_ids(component_ids)

    return Build(
        id=row.id,
        user_id=row.user_id,
        name=row.name,
        notes=row.notes,
        created_at=row.created_at,
        components=components,
    )


def create(build):
    session = get_session()

    result = session.execute(
        text("INSERT INTO build (user_id, name, notes) VALUES (:user_id, :name, :notes) RETURNING id, created_at"),
        {"user_id": build.user_id, "name": build.name, "notes": build.notes}
    )
    row = result.fetchone()
    build.id = row[0]
    build.created_at = row[1]

    for component in build.components:
        session.execute(
            text("INSERT INTO build_component (build_id, component_id) VALUES (:build_id, :component_id)"),
            {"build_id": build.id, "component_id": component.id}
        )

    session.commit()
    session.close()

    return build


def get_all():
    session = get_session()
    rows = session.execute(text("SELECT * FROM build")).fetchall()
    session.close()
    return [_load_build(r) for r in rows]


def get_by_id(build_id):
    session = get_session()
    row = session.execute(
        text("SELECT * FROM build WHERE id = :id"),
        {"id": build_id}
    ).fetchone()
    session.close()

    if row is None:
        return None
    return _load_build(row)


def get_by_user_id(user_id):
    session = get_session()
    rows = session.execute(
        text("SELECT * FROM build WHERE user_id = :user_id"),
        {"user_id": user_id}
    ).fetchall()
    session.close()
    return [_load_build(r) for r in rows]


def update(build_id, data, new_components=None):
    session = get_session()

    fields = []
    params = {"id": build_id}

    if "name" in data:
        fields.append("name = :name")
        params["name"] = data["name"]

    if "notes" in data:
        fields.append("notes = :notes")
        params["notes"] = data["notes"]

    if fields:
        session.execute(
            text(f"UPDATE build SET {', '.join(fields)} WHERE id = :id"),
            params
        )

    if new_components is not None:
        session.execute(text("DELETE FROM build_component WHERE build_id = :id"), {"id": build_id})
        for component in new_components:
            session.execute(
                text("INSERT INTO build_component (build_id, component_id) VALUES (:build_id, :component_id)"),
                {"build_id": build_id, "component_id": component.id}
            )

    session.commit()
    session.close()

    return get_by_id(build_id)


def delete_by_id(build_id):
    session = get_session()
    session.execute(text("DELETE FROM build_component WHERE build_id = :id"), {"id": build_id})
    session.execute(text("DELETE FROM build WHERE id = :id"), {"id": build_id})
    session.commit()
    session.close()
