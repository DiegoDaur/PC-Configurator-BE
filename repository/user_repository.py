from flask import session
from sqlalchemy import text
from persistence.db_config import get_session
from model.user import User


def _row_to_user(row):
    return User(
        id=row.id,
        username=row.username,
        email=row.email,
        password=row.password,
        role=row.role,
    )


def create(user):
    session = get_session()

    result = session.execute(
        text(
            "INSERT INTO \"user\" (username, email, password, role) "
            "VALUES (:username, :email, :password, :role) RETURNING id"
        ),
        {
            "username": user.username,
            "email":    user.email,
            "password": user.password,
            "role":     user.role,
        }
    )
    session.commit()
    user.id = result.fetchone()[0]
    session.close()

    return user


def get_all():
    session = get_session()
    rows = session.execute(text("SELECT * FROM \"user\"")).fetchall()
    session.close()
    return [_row_to_user(r) for r in rows]


def get_by_id(user_id):
    session = get_session()
    row = session.execute(
        text("SELECT * FROM \"user\" WHERE id = :id"),
        {"id": user_id}
    ).fetchone()
    session.close()

    if row is None:
        return None
    return _row_to_user(row)


def get_by_email(email):
    session = get_session()
    row = session.execute(
        text("SELECT * FROM \"user\" WHERE email = :email"),
        {"email": email}
    ).fetchone()
    session.close()

    if row is None:
        return None
    return _row_to_user(row)


def get_by_username(username):
    session = get_session()
    row = session.execute(
        text("SELECT * FROM \"user\" WHERE username = :username"),
        {"username": username}
    ).fetchone()
    session.close()

    if row is None:
        return None
    return _row_to_user(row)


def update(user_id, data):
    session = get_session()

    fields = []
    params = {"id": user_id}

    for campo in ["username", "role"]:
        if campo in data:
            fields.append(f"{campo} = :{campo}")
            params[campo] = data[campo]

    if fields:
        session.execute(
            text(f"UPDATE \"user\" SET {', '.join(fields)} WHERE id = :id"),
            params
        )
        session.commit()

    session.close()
    return get_by_id(user_id)


def delete_by_id(user_id):
    session = get_session()
    session.execute(text("""
    DELETE FROM "build_component" 
    WHERE build_id IN (SELECT id FROM "build" WHERE user_id = :id)
    """), {"id": user_id})
    session.execute(text("DELETE FROM \"build\" WHERE user_id = :id"), {"id": user_id})
    session.execute(text("DELETE FROM \"user\" WHERE id = :id"), {"id": user_id})
    session.commit()
    session.close()
