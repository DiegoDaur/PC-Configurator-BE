from sqlalchemy import text
from persistence.db_config import get_session
from model.compatibility_rule import CompatibilityRule


def _row_to_rule(row):
    return CompatibilityRule(
        id=row.id,
        component_a_id=row.component_a_id,
        component_b_id=row.component_b_id,
        is_compatible=row.is_compatible,
        reason=row.reason,
    )


def create(rule):
    session = get_session()

    result = session.execute(
        text(
            "INSERT INTO compatibility_rule (component_a_id, component_b_id, is_compatible, reason) "
            "VALUES (:a, :b, :compat, :reason) RETURNING id"
        ),
        {
            "a":      rule.component_a_id,
            "b":      rule.component_b_id,
            "compat": rule.is_compatible,
            "reason": rule.reason,
        }
    )
    session.commit()
    rule.id = result.fetchone()[0]
    session.close()

    return rule


def get_all():
    session = get_session()
    rows = session.execute(text("SELECT * FROM compatibility_rule")).fetchall()
    session.close()
    return [_row_to_rule(r) for r in rows]


def get_by_id(rule_id):
    session = get_session()
    row = session.execute(
        text("SELECT * FROM compatibility_rule WHERE id = :id"),
        {"id": rule_id}
    ).fetchone()
    session.close()

    if row is None:
        return None
    return _row_to_rule(row)


def get_rules_for_component(component_id):
    session = get_session()
    rows = session.execute(
        text("SELECT * FROM compatibility_rule WHERE component_a_id = :id OR component_b_id = :id"),
        {"id": component_id}
    ).fetchall()
    session.close()
    return [_row_to_rule(r) for r in rows]


def get_rule_between(id_a, id_b):
    session = get_session()
    row = session.execute(
        text(
            "SELECT * FROM compatibility_rule "
            "WHERE (component_a_id = :a AND component_b_id = :b) "
            "   OR (component_a_id = :b AND component_b_id = :a) "
            "LIMIT 1"
        ),
        {"a": id_a, "b": id_b}
    ).fetchone()
    session.close()

    if row is None:
        return None
    return _row_to_rule(row)


def update(rule_id, data):
    session = get_session()

    fields = []
    params = {"id": rule_id}

    if "is_compatible" in data:
        fields.append("is_compatible = :is_compatible")
        params["is_compatible"] = data["is_compatible"]

    if "reason" in data:
        fields.append("reason = :reason")
        params["reason"] = data["reason"]

    if fields:
        session.execute(
            text(f"UPDATE compatibility_rule SET {', '.join(fields)} WHERE id = :id"),
            params
        )
        session.commit()

    session.close()
    return get_by_id(rule_id)


def delete_by_id(rule_id):
    session = get_session()
    session.execute(text("DELETE FROM compatibility_rule WHERE id = :id"), {"id": rule_id})
    session.commit()
    session.close()
